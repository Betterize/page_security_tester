export { showWhenInView, CSS_CLASS_SHOW };

// ----------------------------------------------------------------------------
// To 'register' new CSS class:
// 1. Add new CSS_CLASS_XXX definition
// 2. Add this definition to the knownCssClasses list
// 3. Add this definition to the exported entities
// E.g.:
// export { showWhenInView, CSS_CLASS_SHOW, CSS_CLASS_SHOW2 };
// ...
// const CSS_CLASS_SHOW2 = "pokaz2";
// ...
// const knownCssClasses = [CSS_CLASS_SHOW, CSS_CLASS_SHOW2];
//
const CSS_CLASS_SHOW = "pokaz";
const knownCssClasses = [CSS_CLASS_SHOW];

// ----------------------------------------------------------------------------
type CssClassName = string;
type Observers = Map<CssClassName, IntersectionObserver>;

const observers = buildObservers(knownCssClasses);

// ----------------------------------------------------------------------------

function showWhenInView(
    queriedClass: CssClassName,
    showClass: CssClassName
): void {
    const observer = observers.get(showClass);

    if (observer == undefined) {
        console.error(
            `Developer errror. Unknown CSS class "${showClass}". Known classes in scroll.ts: ${knownCssClasses}`
        );
        return;
    }

    const notYetShownElements = document.querySelectorAll(queriedClass);
    notYetShownElements.forEach((el) => observer.observe(el));
}

// ----------------------------------------------------------------------------

function buildObservers(classNames: CssClassName[]): Observers {
    const observers: Observers = new Map<CssClassName, IntersectionObserver>();

    classNames.forEach((className) =>
        observers.set(className, buildObserver(className))
    );

    return observers;
}

function buildObserver(className: CssClassName): IntersectionObserver {
    return new IntersectionObserver((entries, observer) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add(className);
                observer.unobserve(entry.target); // przestajemy obserwować element, gdy został już pokazany
            }
        });
    });
}
