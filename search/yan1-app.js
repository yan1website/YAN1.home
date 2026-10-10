(function () {
    if (window.top !== window.self) return;

    function isYAN1App() {
        return window.AndroidPython && typeof window.AndroidPython.executePython === "function";
    }

    function openInYAN1App() {
        if (isYAN1App()) return;

        try {
            const pageKey = `yan1_launched:${window.location.pathname}${window.location.search}`;
            if (sessionStorage.getItem(pageKey) === "true") return;
            sessionStorage.setItem(pageKey, "true");
        } catch (error) {
            // Continue when session storage is unavailable.
        }

        const currentURL = window.location.href;
        const cleanPath = currentURL.replace(/^https?:\/\//, "");
        const fallbackURL = new URL("/YAN1.home/download_app.html", window.location.origin).href;
        const intentURL = "intent://" + cleanPath + "#Intent;scheme=https;package=com.example1.yan1appgen1;S.browser_fallback_url=" + encodeURIComponent(fallbackURL) + ";end;";
        window.location.href = intentURL;
    }

    setTimeout(openInYAN1App, 1200);
})();
