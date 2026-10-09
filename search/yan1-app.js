(function () {
    if (window.top !== window.self) return;

    function isYAN1App() {
        return window.AndroidPython && typeof window.AndroidPython.executePython === "function";
    }

    function openInYAN1App() {
        if (isYAN1App()) return;

        try {
            if (sessionStorage.getItem("yan1_launched") === "true") return;
            sessionStorage.setItem("yan1_launched", "true");
        } catch (error) {
            // Continue when session storage is unavailable.
        }

        const currentURL = window.location.href;
        const cleanPath = currentURL.replace(/^https?:\/\//, "");
        const intentURL = "intent://" + cleanPath + "#Intent;scheme=https;package=com.example1.yan1appgen1;S.browser_fallback_url=" + encodeURIComponent(currentURL) + ";end;";
        window.location.href = intentURL;
    }

    setTimeout(openInYAN1App, 1200);
})();
