export function isMobileDevice() {
    let regexp = /android|iphone|kindle|ipad/i;

    return regexp.test(navigator.userAgent) || window.innerWidth <= 480;
}
