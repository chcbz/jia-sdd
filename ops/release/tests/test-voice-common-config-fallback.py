#!/usr/bin/python3
"""Pure-offline parity matrix for the two real embedded voice config parsers."""

from pathlib import Path
import base64
import os
import subprocess
import sys
import tempfile
import unittest


RELEASE = Path(__file__).resolve().parents[1]
PARSER_PATHS = (
    ("lifecycle", RELEASE / "host" / "cyf-api-kit", "load_voice_environment() {", False),
    ("transaction", RELEASE / "lib" / "api-host-transaction.sh", "host_parse_voice_config() {", True),
)
DEFERRED_MARKER = "VOICE_PROVIDER_CONNECTION_VALIDATION=APPLICATION_STARTUP_REQUIRED"
IDENTITY = "I" * 32
CACHE = base64.b64encode(b"C" * 32).decode("ascii")
COMMON_KEY = "provider-common-test-key"
TRANSCRIPTION_KEY = "provider-transcription-test-key"
SPEECH_KEY = "provider-speech-test-key"
OPENAI_URL = "https://api.openai.com/v1"
COMPAT_URL = "https://voice-gateway.example/openai/v1"
CONNECTION_NAMES = (
    "SPRING_AI_OPENAI_API_KEY",
    "SPRING_AI_OPENAI_BASE_URL",
    "SPRING_AI_OPENAI_AUDIO_TRANSCRIPTION_API_KEY",
    "SPRING_AI_OPENAI_AUDIO_TRANSCRIPTION_BASE_URL",
    "SPRING_AI_OPENAI_AUDIO_SPEECH_API_KEY",
    "SPRING_AI_OPENAI_AUDIO_SPEECH_BASE_URL",
)
KEY_NAMES = CONNECTION_NAMES[0], CONNECTION_NAMES[2], CONNECTION_NAMES[4]
URL_NAMES = CONNECTION_NAMES[1], CONNECTION_NAMES[3], CONNECTION_NAMES[5]


def extract_parser(path, function_marker):
    text = path.read_text(encoding="utf-8")
    function_start = text.index(function_marker)
    body_start = text.index("<<'PY'\n", function_start) + len("<<'PY'\n")
    body_end = text.index("\nPY\n", body_start)
    body = text[body_start:body_end]
    compile(body, str(path) + "::<embedded-parser>", "exec")
    return body


def base_values():
    return {
        "JIA_CHAT_VOICE_ENABLED": "true",
        "JIA_CHAT_VOICE_IDENTITY_HMAC_SECRET": IDENTITY,
        "JIA_CHAT_VOICE_CACHE_ENCRYPTION_KEY": CACHE,
        "JIA_CHAT_VOICE_COMPATIBILITY_GATEWAY_ALLOWLIST": OPENAI_URL,
        "JIA_CHAT_VOICE_TRANSCRIPTION_ENABLED": "true",
        "JIA_CHAT_VOICE_TRANSCRIPTION_PROVIDER": "openai-compatible",
        "JIA_CHAT_VOICE_TRANSCRIPTION_MODEL": "whisper-1",
        "JIA_CHAT_VOICE_SYNTHESIS_ENABLED": "true",
        "JIA_CHAT_VOICE_SYNTHESIS_PROVIDER": "openai-compatible",
        "JIA_CHAT_VOICE_SYNTHESIS_MODEL": "gpt-4o-mini-tts",
        "JIA_CHAT_VOICE_SYNTHESIS_PROVIDER_VOICE": "alloy",
        "CYF_VOICE_SMOKE_BEARER_TOKEN": "smoke-test-bearer",
    }


def full_explicit_values():
    values = base_values()
    values.update({
        "SPRING_AI_OPENAI_API_KEY": COMMON_KEY,
        "SPRING_AI_OPENAI_BASE_URL": OPENAI_URL,
        "SPRING_AI_OPENAI_AUDIO_TRANSCRIPTION_API_KEY": TRANSCRIPTION_KEY,
        "SPRING_AI_OPENAI_AUDIO_TRANSCRIPTION_BASE_URL": OPENAI_URL,
        "SPRING_AI_OPENAI_AUDIO_SPEECH_API_KEY": SPEECH_KEY,
        "SPRING_AI_OPENAI_AUDIO_SPEECH_BASE_URL": OPENAI_URL,
    })
    return values


def encode_values(values):
    return "".join("{}={}\n".format(name, values[name]) for name in sorted(values)).encode("utf-8")


def decode_assignments(stdout):
    result = {}
    for encoded in stdout.decode("ascii").splitlines():
        assignment = base64.b64decode(encoded, validate=True).decode("utf-8")
        name, separator, value = assignment.partition("=")
        if not separator or name in result:
            raise AssertionError("invalid parser assignment output")
        result[name] = value
    return result


class VoiceCommonConfigFallbackTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parsers = []
        for name, path, marker, has_mode in PARSER_PATHS:
            cls.parsers.append((name, extract_parser(path, marker), has_mode))

    def execute(self, parser, has_mode, payload):
        fd, config_path = tempfile.mkstemp(prefix="voice-common-fallback-", suffix=".env")
        try:
            with os.fdopen(fd, "wb") as stream:
                fd = None
                stream.write(payload)
            command = ["/usr/bin/python3", "-I", "-B", "-", config_path]
            if has_mode:
                command.append("java")
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            stdout, stderr = process.communicate(parser.encode("utf-8"))
            return process.returncode, stdout, stderr.decode("utf-8", "replace")
        finally:
            if fd is not None:
                os.close(fd)
            os.unlink(config_path)

    def assert_case(self, name, payload, accepted, deferred=False):
        outcomes = []
        for parser_name, parser, has_mode in self.parsers:
            with self.subTest(case=name, parser=parser_name):
                rc, stdout, stderr = self.execute(parser, has_mode, payload)
                self.assertEqual(rc == 0, accepted, (rc, stdout, stderr))
                for secret in (IDENTITY, CACHE, COMMON_KEY, TRANSCRIPTION_KEY, SPEECH_KEY,
                               "smoke-test-bearer", "must-not-print"):
                    self.assertNotIn(secret, stderr)
                if accepted:
                    decoded = decode_assignments(stdout)
                    self.assertNotIn("CYF_VOICE_SMOKE_BEARER_TOKEN", decoded)
                    self.assertEqual(
                        decoded,
                        {key: value for key, value in parse_payload(payload).items()
                         if key != "CYF_VOICE_SMOKE_BEARER_TOKEN"})
                    self.assertEqual(DEFERRED_MARKER in stderr, deferred, stderr)
                    outcomes.append(decoded)
                else:
                    self.assertEqual(stdout, b"")
        if accepted:
            self.assertEqual(outcomes[0], outcomes[1], name)

    def test_success_matrix(self):
        full = full_explicit_values()
        cases = []
        cases.append(("all-explicit", encode_values(full), False))

        common_only = base_values()
        common_only.update({
            "SPRING_AI_OPENAI_API_KEY": COMMON_KEY,
            "SPRING_AI_OPENAI_BASE_URL": OPENAI_URL,
        })
        cases.append(("explicit-common-with-audio-inheritance", encode_values(common_only), False))

        audio_only = base_values()
        audio_only.update({
            "SPRING_AI_OPENAI_AUDIO_TRANSCRIPTION_API_KEY": TRANSCRIPTION_KEY,
            "SPRING_AI_OPENAI_AUDIO_TRANSCRIPTION_BASE_URL": OPENAI_URL,
            "SPRING_AI_OPENAI_AUDIO_SPEECH_API_KEY": SPEECH_KEY,
            "SPRING_AI_OPENAI_AUDIO_SPEECH_BASE_URL": OPENAI_URL,
        })
        cases.append(("explicit-audio-connections-with-common-absent", encode_values(audio_only), False))

        cases.append(("application-common-inheritance", encode_values(base_values()), True))

        transcription_override = base_values()
        transcription_override.update({
            "SPRING_AI_OPENAI_AUDIO_TRANSCRIPTION_API_KEY": TRANSCRIPTION_KEY,
            "SPRING_AI_OPENAI_AUDIO_TRANSCRIPTION_BASE_URL": OPENAI_URL,
        })
        cases.append(("transcription-only-override", encode_values(transcription_override), True))

        speech_override = base_values()
        speech_override.update({
            "SPRING_AI_OPENAI_AUDIO_SPEECH_API_KEY": SPEECH_KEY,
            "SPRING_AI_OPENAI_AUDIO_SPEECH_BASE_URL": COMPAT_URL,
            "JIA_CHAT_VOICE_COMPATIBILITY_GATEWAY_ALLOWLIST": OPENAI_URL + "," + COMPAT_URL,
        })
        cases.append(("speech-only-override", encode_values(speech_override), True))

        mixed = dict(common_only)
        mixed.update({
            "SPRING_AI_OPENAI_AUDIO_TRANSCRIPTION_API_KEY": TRANSCRIPTION_KEY,
            "SPRING_AI_OPENAI_AUDIO_TRANSCRIPTION_BASE_URL": COMPAT_URL,
            "JIA_CHAT_VOICE_COMPATIBILITY_GATEWAY_ALLOWLIST": OPENAI_URL + "," + COMPAT_URL,
        })
        cases.append(("partial-audio-override-over-explicit-common", encode_values(mixed), False))

        compat = base_values()
        compat.update({
            "SPRING_AI_OPENAI_API_KEY": COMMON_KEY,
            "SPRING_AI_OPENAI_BASE_URL": COMPAT_URL,
            "JIA_CHAT_VOICE_COMPATIBILITY_GATEWAY_ALLOWLIST": COMPAT_URL,
        })
        cases.append(("normalized-allowlisted-compatibility-url", encode_values(compat), False))

        commented = b"# private voice overrides; common connection remains in application config\n\n" \
            + encode_values(base_values())
        cases.append(("comments-and-empty-lines", commented, True))

        for name, payload, deferred in cases:
            self.assert_case(name, payload, True, deferred)

    def test_explicit_blank_invalid_and_secret_aliases_fail_closed(self):
        for key_name in KEY_NAMES:
            for value_name, value in (("empty", ""), ("blank", "   "), ("identity-alias", IDENTITY)):
                values = full_explicit_values()
                values[key_name] = value
                self.assert_case("{}-{}".format(key_name, value_name), encode_values(values), False)

        for url_name in URL_NAMES:
            values = full_explicit_values()
            values[url_name] = ""
            self.assert_case("{}-blank".format(url_name), encode_values(values), False)

        cache_alias = full_explicit_values()
        cache_alias["JIA_CHAT_VOICE_IDENTITY_HMAC_SECRET"] = "C" * 32
        self.assert_case("identity-aliases-decoded-cache", encode_values(cache_alias), False)

    def test_url_normalization_and_allowlist_fail_closed(self):
        unsafe_urls = (
            "http://api.openai.com/v1",
            "https://user@api.openai.com/v1",
            "https://api.openai.com/v1?target=/audio/speech",
            "https://api.openai.com/v1#target",
            "https://api.openai.com/v1/",
            "https://api.openai.com/openai/../v1",
            "https://api.openai.com/openai%2Fv1",
            "https://api.openai.com/openai//v1",
            "https://api.openai.com/openai\\v1",
            "https://api.openai.com/openai;v1",
        )
        for index, url in enumerate(unsafe_urls):
            values = full_explicit_values()
            values[URL_NAMES[index % len(URL_NAMES)]] = url
            values["JIA_CHAT_VOICE_COMPATIBILITY_GATEWAY_ALLOWLIST"] = ",".join((OPENAI_URL, url))
            self.assert_case("unsafe-url-{}".format(index), encode_values(values), False)

        unallowlisted = full_explicit_values()
        unallowlisted["SPRING_AI_OPENAI_AUDIO_SPEECH_BASE_URL"] = COMPAT_URL
        self.assert_case("unallowlisted-audio-url", encode_values(unallowlisted), False)

    def test_existing_activation_identity_cache_flag_provider_model_and_smoke_rules(self):
        mutations = (
            ("master-flag", "JIA_CHAT_VOICE_ENABLED", "false"),
            ("transcription-flag", "JIA_CHAT_VOICE_TRANSCRIPTION_ENABLED", "false"),
            ("synthesis-flag", "JIA_CHAT_VOICE_SYNTHESIS_ENABLED", "false"),
            ("transcription-provider", "JIA_CHAT_VOICE_TRANSCRIPTION_PROVIDER", "disabled"),
            ("synthesis-provider", "JIA_CHAT_VOICE_SYNTHESIS_PROVIDER", "disabled"),
            ("transcription-model", "JIA_CHAT_VOICE_TRANSCRIPTION_MODEL", "other"),
            ("synthesis-model", "JIA_CHAT_VOICE_SYNTHESIS_MODEL", "other"),
            ("synthesis-voice", "JIA_CHAT_VOICE_SYNTHESIS_PROVIDER_VOICE", "other"),
            ("short-identity", "JIA_CHAT_VOICE_IDENTITY_HMAC_SECRET", "short"),
            ("invalid-cache", "JIA_CHAT_VOICE_CACHE_ENCRYPTION_KEY", "not-base64"),
            ("short-cache", "JIA_CHAT_VOICE_CACHE_ENCRYPTION_KEY",
             base64.b64encode(b"short").decode("ascii")),
            ("blank-smoke", "CYF_VOICE_SMOKE_BEARER_TOKEN", ""),
        )
        for name, key, value in mutations:
            values = full_explicit_values()
            values[key] = value
            self.assert_case(name, encode_values(values), False)

        missing_smoke = full_explicit_values()
        del missing_smoke["CYF_VOICE_SMOKE_BEARER_TOKEN"]
        self.assert_case("missing-smoke", encode_values(missing_smoke), False)

    def test_unknown_duplicate_assignment_utf8_and_control_bytes_fail_closed(self):
        valid = encode_values(full_explicit_values())
        payloads = (
            ("unknown-name", valid + b"UNKNOWN_SECRET=must-not-print\n"),
            ("duplicate-name", valid + b"JIA_CHAT_VOICE_ENABLED=true\n"),
            ("invalid-assignment", valid + b"not-an-assignment\n"),
            ("invalid-utf8", valid + b"UNKNOWN_SECRET=\xff\n"),
            ("nul-control", valid + b"SPRING_AI_OPENAI_API_KEY=bad\x00key\n"),
            ("tab-control", valid + b"SPRING_AI_OPENAI_API_KEY=bad\tkey\n"),
            ("delete-control", valid + b"SPRING_AI_OPENAI_API_KEY=bad\x7fkey\n"),
        )
        for name, payload in payloads:
            self.assert_case(name, payload, False)


def parse_payload(payload):
    values = {}
    for raw in payload.splitlines():
        if not raw or raw.startswith(b"#"):
            continue
        line = raw.decode("utf-8")
        name, separator, value = line.partition("=")
        if separator:
            values[name] = value
    return values


if __name__ == "__main__":
    unittest.main(verbosity=2)
