# Entry contract

- Cold launch: `https://kit.chaoyoufan.cn/?nativeOrientation=portrait&entry=direct`.
- `/`: product introduction for guests (the upstream valid-session guard sends logged-in users to `/juyiting` while retaining query/hash), concrete example and use cases; `/demo`: local four-step simulation; `/juyiting`: real workbench with existing authentication.
- Public links carry only `nativeOrientation=portrait` and `entry=direct|fallback`. Source query credentials, arbitrary redirects, arrays and invalid markers are not forwarded. Only a locally allowlisted sample template can be added for onboarding; it does not create a task.
- Native landscape stays on its fixed landscape page. Failed return fallback loads `/juyiting?nativeOrientation=portrait&entry=fallback`, not `/`.
- Step changes focus the new heading and scroll it into view. Back/restart retain the selected template. Responsive layouts cover narrow mobile and desktop widths.
- API method/path, request/response/events, error behavior, authentication/authorization, and asynchronous replay/version semantics: unchanged. No migrations or ACL changes.
- Release requires both Web and Mini Program packages; local tests cannot prove physical-device orientation or business-domain configuration.
