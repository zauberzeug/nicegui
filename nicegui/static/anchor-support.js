class AnchorSupport {
    /*
    This class has two main functions:

    - Record size of elements as they change, so that the size is available for positioning.
    - Enable dynamic sizing of elements with position: absolute children.
    */

    constructor() {
        this.INTERNAL_WIDTH_VARIABLE = "--internal-width-";
        this.EXTERNAL_WIDTH_VARIABLE = "--external-width-";
        this.INTERNAL_HEIGHT_VARIABLE = "--internal-height-";
        this.EXTERNAL_HEIGHT_VARIABLE = "--external-height-";
        this.DYNAMIC_HEIGHT_CLASS = "dynamic-height";
        this.DYNAMIC_WIDTH_CLASS = "dynamic-width";
        this.DYNAMIC_SIZE_CLASS = "dynamic-size";
        this.IGNORE_FOR_SIZE_CLASS = "ignore-for-size"

        this.dirtyDynamicHeight = new Set();
        this.dirtyDynamicWidth = new Set();
        this.intersectionObservers = {};

        // Create initial observers
        this.newElementsObserver = new MutationObserver(
            this.classChangeHandler.bind(this)
        ).observe(document, {childList: true, subtree: true});
        this.anchorsResizeExternalObserver = new ResizeObserver(this.resizeExternalEntriesHandler.bind(this));
        this.anchorsResizeInternalObserver = new ResizeObserver(this.resizeInternalEntriesHandler.bind(this));
    }

    classChangeHandler(mutations, observer) {
        // Start watching resizes of all added elements with ID
        mutations.forEach((mutation) => {
            if (mutation.type === "childList") {
                mutation.addedNodes.forEach((notifiedNode) => {
                    const toObserve = new Set();
                    toObserve.add(notifiedNode);
                    while (toObserve.size > 0) {
                        toObserve.forEach(node => {
                            toObserve.delete(node);
                            if (node.getAttribute) {
                                const nodeID = node.id;
                                if (nodeID) {
                                    this.anchorsResizeExternalObserver.observe(node, {box: "border-box"});
                                    this.anchorsResizeInternalObserver.observe(node, {box: "content-box"});
                                    for (let i = 0; i < node.children.length; i++) {
                                        toObserve.add(node.children[i]);
                                    }
                                }
                            }
                        });
                    }
                });
            }
        });
    }

    resizeExternalEntriesHandler(entries) {
        // Record external and internal size of elements in CSS variables
        const root = document.documentElement;
        entries.forEach((entry) => {
            const node = entry.target;
            this.parentResizeKicker(node);
            this.setIntersectionObserver(node);

            const nodeID = node.id;

            const borderSize = entry.borderBoxSize[0];
            if (borderSize) {
                root.style.setProperty(this.EXTERNAL_WIDTH_VARIABLE + nodeID, borderSize.inlineSize + "px")
                root.style.setProperty(this.EXTERNAL_HEIGHT_VARIABLE + nodeID, borderSize.blockSize + "px")
            }
        });
        requestAnimationFrame(this.updateDynamicSize.bind(this));
    }

    resizeInternalEntriesHandler(entries) {
        // Record external and internal size of elements in CSS variables
        const root = document.documentElement;
        entries.forEach((entry) => {
            const node = entry.target;
            this.parentResizeKicker(node);

            const nodeID = node.id;

            const contentSize = entry.contentBoxSize[0];
            if (contentSize) {
                root.style.setProperty(this.INTERNAL_WIDTH_VARIABLE + nodeID, contentSize.inlineSize + "px")
                root.style.setProperty(this.INTERNAL_HEIGHT_VARIABLE + nodeID, contentSize.blockSize + "px")
            }
        });
        requestAnimationFrame(this.updateDynamicSize.bind(this));
    }

    parentResizeKicker(node) {
        // Based on element class, request refreshing width, height or both.
        const parent = node.parentNode;
        if (parent) {
            const classes = parent.classList;
            if (classes.contains(this.DYNAMIC_HEIGHT_CLASS)) {
                this.dirtyDynamicHeight.add(parent);
            }
            if (classes.contains(this.DYNAMIC_WIDTH_CLASS)) {
                this.dirtyDynamicWidth.add(parent);
            }
            if (classes.contains(this.DYNAMIC_SIZE_CLASS)) {
                this.dirtyDynamicHeight.add(parent);
                this.dirtyDynamicWidth.add(parent);
            }
        }
    }

    setIntersectionObserver(node) {
        // Re-set full containment observer every time handler is triggered to handle animations etc.
        const parent = node.parentNode;
        const nodeID = node.id;
        if (parent && nodeID) {
            let observer = this.intersectionObservers[nodeID];
            if (observer) {
                observer.disconnect();
            }
            observer = new IntersectionObserver(this.intersectionHandler.bind(this), {
                root: parent,
                threshold: 1.0
            });
            this.intersectionObservers[nodeID] = observer;
            observer.observe(node);
        }
    }

    intersectionHandler(entries, observer) {
        // Trigger parent resize when child is no longer completely contained
        entries.forEach(entry => {
            if (entry.intersectionRatio < 1.0) {
                this.parentResizeKicker(entry.target);
                this.setIntersectionObserver(entry.target);
            }
        });
        requestAnimationFrame(this.updateDynamicSize.bind(this));
    }

    updateDynamicSize() {
        // Update parent dimension(s) to cover all (positioned) child elements with ID
        const root = document.documentElement;
        const rootStyle = getComputedStyle(root);
        this.dirtyDynamicHeight.forEach(node => {
            const children = node.children;
            let height = 0;

            for (let i = 0; i < children.length; i++) {
                const child = children[i];
                const nodeID = child.id;
                if (!nodeID) continue;
                const classes = child.classList;
                if (classes.contains(this.IGNORE_FOR_SIZE_CLASS)) continue;

                const style = window.getComputedStyle(child);
                const varName = this.EXTERNAL_HEIGHT_VARIABLE + nodeID;
                const varValue = rootStyle.getPropertyValue(varName);
                const externalHeight = varValue ? parseFloat(varValue) : 0;
                const top = style.top ? parseFloat(style.top) : 0;
                const topMargin = style.marginTop ? parseFloat(style.marginTop) : 0;
                const bottomMargin = style.marginBottom ? parseFloat(style.marginBottom) : 0;

                const childBottom = top + topMargin + externalHeight + bottomMargin;
                height = Math.max(height, childBottom);
            }
            node.style.minHeight = "" + height + "px";
        });
        this.dirtyDynamicWidth.forEach(node => {
            const children = node.children;
            let width = 0;

            for (let i = 0; i < children.length; i++) {
                const child = children[i];
                const nodeID = child.id;
                if (!nodeID) continue;

                const style = window.getComputedStyle(child);
                const varName = this.EXTERNAL_WIDTH_VARIABLE + nodeID;
                const varValue = rootStyle.getPropertyValue(varName);
                const externalWidth = varValue ? parseFloat(varValue) : 0;
                const left = style.left ? parseFloat(style.left) : 0;
                const leftMargin = style.marginLeft ? parseFloat(style.marginLeft) : 0;
                const rightMargin = style.marginRight ? parseFloat(style.marginRight) : 0;

                const childRight = left + leftMargin + externalWidth + rightMargin;
                width = Math.max(width, childRight);
            }
            node.style.minWidth = "" + width + "px";
        });
        this.dirtyDynamicHeight.clear();
        this.dirtyDynamicWidth.clear();
    }
}

var anchorSupport = new AnchorSupport();
