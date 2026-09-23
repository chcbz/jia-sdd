#!/usr/bin/env python3
"""Check actual Chromium tab zoom=200% on local Vue, without live API or credentials.

A temporary MV3 extension calls chrome.tabs.setZoom(2) and getZoom(); no CSS zoom,
page-scale emulation, or viewport-halving shortcut is used. Requires a fresh Vite
server for this worktree and the system Chromium/Playwright (not CI Chrome 133).
"""
import argparse
import json
import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

WEB_SHA = '8f47a1289bf501616ba234638192a5303d3155d7'
SIZES = [(320, 740), (390, 844), (844, 390), (1440, 900)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default='https://127.0.0.1:61360')
    parser.add_argument('--chromium', default=shutil.which('chromium'))
    parser.add_argument('--out', type=Path, help='Save safe, local-only geometry JSON')
    parser.add_argument('--screenshots', type=Path, help='Save two local-only screenshots')
    args = parser.parse_args()
    url = urlparse(args.url)
    if url.scheme not in ('https', 'http') or url.hostname not in ('localhost', '127.0.0.1', '::1') or url.username or url.password:
        parser.error('Only a loopback origin without credentials is allowed')
    if not args.chromium:
        parser.error('Specify --chromium PATH')
    web_dir = Path(__file__).resolve().parents[3] / 'web'
    actual_sha = subprocess.check_output(['git', '-C', str(web_dir), 'rev-parse', 'HEAD'], text=True).strip()
    if actual_sha != WEB_SHA:
        parser.error(f'Expected local web HEAD {WEB_SHA}; got {actual_sha}')
    origin = f'{url.scheme}://{url.netloc}'
    results = []
    with TemporaryDirectory(prefix='cyf-actual-zoom-') as temp, sync_playwright() as playwright:
        extension = Path(temp) / 'extension'
        extension.mkdir()
        (extension / 'manifest.json').write_text(json.dumps({
            'manifest_version': 3, 'name': 'CYF offline zoom measurement', 'version': '1.0',
            'permissions': ['tabs'], 'background': {'service_worker': 'worker.js'},
        }))
        (extension / 'worker.js').write_text('chrome.runtime.onInstalled.addListener(() => {});')
        for width, height in SIZES:
            context = playwright.chromium.launch_persistent_context(
                str(Path(temp) / f'profile-{width}'), executable_path=args.chromium,
                headless=True, viewport={'width': width, 'height': height},
                device_scale_factor=1, ignore_https_errors=True,
                args=[f'--disable-extensions-except={extension}', f'--load-extension={extension}'],
            )
            try:
                context.add_init_script("if (location.origin === " + json.dumps(origin) +
                    " && window.top === window) { localStorage.setItem('api_token', JSON.stringify({data:'local-layout-only',expTime:Date.now()+120000})); " +
                    "if ('serviceWorker' in navigator) navigator.serviceWorker.register = () => Promise.reject(new Error('Local probe blocks app service workers')); }")

                intercepted = {'GET': 0, 'POST': 0, 'other': 0}

                def route_request(route):
                    target = route.request.url
                    parsed = urlparse(target)
                    path = parsed.path
                    if f'{parsed.scheme}://{parsed.netloc}' != origin:
                        route.abort()
                    elif (route.request.resource_type in ('xhr', 'fetch') or
                            path.startswith(('/api/', '/chat/', '/agent/', '/user/', '/task/', '/oauth2/'))):
                        method = route.request.method
                        intercepted[method if method in intercepted else 'other'] += 1
                        route.fulfill(status=200, content_type='application/json', body='{"code":200,"data":[],"items":[]}')
                    elif target.startswith(origin + '/'):
                        route.continue_()
                    else:
                        route.abort()

                context.route('**/*', route_request)
                page = context.new_page()
                page.goto(origin + '/juyiting', wait_until='domcontentloaded', timeout=30000)
                assert page.evaluate('''() => !!document.querySelector('script[src*="/@vite/client"]') &&
                  (!('serviceWorker' in navigator) || navigator.serviceWorker.controller === null)'''), 'Only fresh Vite dev pages are permitted'
                page.locator('.onboarding-dialog .skip-button').click(timeout=25000)
                page.locator('.onboarding-overlay').wait_for(state='hidden')
                worker = context.service_workers[0] if context.service_workers else context.wait_for_event('serviceworker', timeout=10000)
                tab_zoom = worker.evaluate('''async origin => {
                  const tabs = await chrome.tabs.query({});
                  const tab = tabs.find(t => t.url?.startsWith(origin + '/juyiting'));
                  if (!tab) throw new Error('Local workbench tab not found');
                  await chrome.tabs.setZoom(tab.id, 2);
                  return chrome.tabs.getZoom(tab.id);
                }''', origin)
                page.wait_for_function('''([w,h]) => devicePixelRatio === 2 &&
                    Math.abs(innerWidth * 2 - w) <= 1 &&
                    Math.abs(innerHeight * 2 - h) <= 1''', arg=[width, height], timeout=12000)
                viewport = page.evaluate('''() => ({ devicePixelRatio, innerWidth, innerHeight, outerWidth, outerHeight,
                    visualViewportScale: visualViewport.scale, pageScrollWidth:document.documentElement.scrollWidth,
                    userAgent:navigator.userAgent })''')
                assert tab_zoom == 2 and viewport['visualViewportScale'] == 1, viewport
                assert viewport['pageScrollWidth'] <= viewport['innerWidth'], viewport
                trigger = page.locator('.workbench-mobile-more')
                trigger.click()
                menu = page.locator('.workbench-more-menu')
                menu.wait_for(state='visible')
                last = menu.locator('button').last
                last.scroll_into_view_if_needed()
                last.focus()
                assert last.evaluate('(e) => document.activeElement === e')
                nav_menu = page.evaluate('''() => {
                  const box = s => {const r=document.querySelector(s).getBoundingClientRect();return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,height:r.height}};
                  const tabs=[...document.querySelectorAll('.workbench-mobile-nav button')].map(e=>({
                    label:e.getAttribute('aria-label'), display:getComputedStyle(e.querySelector('span')).display,
                    width:e.getBoundingClientRect().width }));
                  return {header:box('.hall-app-header'),menu:box('.workbench-more-menu'),nav:box('.workbench-mobile-nav'),tabs};
                }''')
                assert nav_menu['header']['left'] >= -.5 and nav_menu['header']['right'] <= viewport['innerWidth'] + .5, nav_menu
                assert nav_menu['menu']['left'] >= -.5 and nav_menu['menu']['right'] <= viewport['innerWidth'] + .5, nav_menu
                assert nav_menu['menu']['bottom'] <= nav_menu['nav']['top'] + .5, nav_menu
                assert [t['label'] for t in nav_menu['tabs']] == ['办事概览', '我的事项', '厅内议事', '典籍阁'], nav_menu
                assert all(t['width'] > 0 for t in nav_menu['tabs']), nav_menu
                if viewport['innerWidth'] <= 240:
                    assert [t['display'] for t in nav_menu['tabs'][:3]] == ['none'] * 3, nav_menu
                assert nav_menu['tabs'][-1]['display'] != 'none', nav_menu
                menu.get_by_role('button', name='厅内议事').click()
                dialog = page.get_by_role('dialog', name='厅内议事')
                assert dialog.count() == 1
                title_id = dialog.get_attribute('aria-labelledby')
                assert title_id and page.evaluate('id => document.getElementById(id)?.textContent?.includes("厅内议事")', title_id)
                # The panel enters with translateY(10px); wait for animation before checking overlap.
                page.wait_for_function('''() => {const a=document.querySelector('.panel-overlay.is-workbench-panel');
                   const b=a?.querySelector('.floating-panel');return b && Math.abs(a.getBoundingClientRect().top-b.getBoundingClientRect().top)<.5}''')
                chat = page.evaluate('''() => {
                  const box=s=>{const r=document.querySelector(s).getBoundingClientRect();return {top:r.top,bottom:r.bottom,height:r.height}};
                  const p=document.querySelector('.panel-overlay.is-workbench-panel > .floating-panel');
                  return {messages:box('.hall-messages'),composer:box('.hall-chat-composer'),overlay:box('.panel-overlay.is-workbench-panel'),
                    windowClientHeight:p.clientHeight,windowScrollHeight:p.scrollHeight,nav:box('.workbench-mobile-nav'),
                    pageScrollWidth:document.documentElement.scrollWidth};
                }''')
                assert chat['pageScrollWidth'] <= viewport['innerWidth'], chat
                if viewport['innerHeight'] <= 260:
                    assert chat['windowScrollHeight'] > chat['windowClientHeight'], chat
                    page.locator('.composer-send').scroll_into_view_if_needed()
                    send_box = page.locator('.composer-send').bounding_box()
                    assert send_box and chat['overlay']['top'] - .5 <= send_box['y'] and send_box['y'] + send_box['height'] <= chat['nav']['top'] + .5, chat
                    chat['windowScrollAfter'] = page.locator('.floating-panel').evaluate('(e) => e.scrollTop')
                    assert chat['windowScrollAfter'] > 0, chat
                else:
                    assert chat['composer']['bottom'] <= chat['nav']['top'] + .5, chat
                    assert chat['messages']['height'] >= 40, chat
                    if viewport['innerWidth'] <= 240:
                        action = page.locator('.chat-panel .toolbar-actions button').last
                        action.scroll_into_view_if_needed()
                        action.focus()
                        assert action.evaluate('(e) => document.activeElement === e')
                        chat['toolbarScrollAfter'] = page.locator('.chat-panel .panel-toolbar').evaluate('(e) => e.scrollLeft')
                        assert chat['toolbarScrollAfter'] > 0, chat
                if args.screenshots and width in (320, 844):
                    args.screenshots.mkdir(parents=True, exist_ok=True)
                    page.screenshot(path=str(args.screenshots / f'actual-zoom-{width}x{height}.png'))
                long_chat = page.evaluate('''() => {
                    const messages=document.querySelector('.hall-messages');
                    for (let i=0;i<28;i++) { const item=document.createElement('p');
                      item.textContent='本地合成消息 '+(i+1)+'：仅用于浏览器缩放时测试长对话滚动，不来自任何用户或服务。';
                      messages.appendChild(item); }
                    const maxScroll=messages.scrollHeight-messages.clientHeight;
                    messages.scrollTop=messages.scrollHeight;
                    return {clientHeight:messages.clientHeight,scrollHeight:messages.scrollHeight,scrollTop:messages.scrollTop,
                      pageScrollWidth:document.documentElement.scrollWidth};
                }''')
                assert long_chat['scrollHeight'] > long_chat['clientHeight'] and long_chat['scrollTop'] > 0, long_chat
                assert long_chat['pageScrollWidth'] <= viewport['innerWidth'], long_chat
                if viewport['innerHeight'] > 260:
                    composer_bottom = page.locator('.hall-chat-composer').bounding_box()
                    assert composer_bottom and composer_bottom['y'] + composer_bottom['height'] <= chat['nav']['top'] + .5, long_chat
                results.append({'baseViewportPixels': f'{width}x{height}', 'tabZoom': tab_zoom,
                                'viewport': viewport, 'navigation': nav_menu, 'chat': chat, 'syntheticLongChat': long_chat,
                                'interceptedApiRequestsByMethod': intercepted})
                print(f'PASS tab zoom 200% {width}x{height} -> {viewport["innerWidth"]}x{viewport["innerHeight"]}')
            finally:
                context.close()
    if args.out:
        args.out.write_text(json.dumps({'webSha': actual_sha, 'browser': 'system Chromium (not project Chrome 133); see results[*].viewport.userAgent for runtime version',
                                        'method': 'chrome.tabs.setZoom(2) and getZoom() using isolated temporary extension',
                                        'limitations': 'local fake token, empty intercepted API, no real keyboard/safe area or service',
                                        'results': results}, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
