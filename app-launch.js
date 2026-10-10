(() => {
  if (window.top !== window.self) return;
  if (window.AndroidPython && typeof window.AndroidPython.executePython === 'function') return;

  const pageURL = new URL(window.location.href);
  if (pageURL.pathname.endsWith('/download_app.html')) return;
  if (pageURL.protocol !== 'http:' && pageURL.protocol !== 'https:') return;
  if (pageURL.hostname === '127.0.0.1' || pageURL.hostname === 'localhost') return;

  const pageKey = `yan1_launched:${pageURL.pathname}${pageURL.search}`;
  try {
    if (sessionStorage.getItem(pageKey) === 'true') return;
    sessionStorage.setItem(pageKey, 'true');
  } catch (_) {}

  const appRootPath = pageURL.pathname.includes('/YAN1.home/')
    ? `${pageURL.pathname.slice(0, pageURL.pathname.indexOf('/YAN1.home/'))}/YAN1.home/`
    : '/YAN1.home/';
  const fallbackURL = new URL('download_app.html', `${pageURL.origin}${appRootPath}`).href;
  const intentURL = `intent://${pageURL.host}${pageURL.pathname}${pageURL.search}#Intent;scheme=${pageURL.protocol.slice(0, -1)};package=com.example1.yan1appgen1;S.browser_fallback_url=${encodeURIComponent(fallbackURL)};end;`;
  setTimeout(() => window.location.replace(intentURL), 1200);
})();