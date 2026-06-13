/*!
    * Start Bootstrap - SB Admin Pro v2.0.4 (https://shop.startbootstrap.com/product/sb-admin-pro)
    * Copyright 2013-2022 Start Bootstrap
    * Licensed under SEE_LICENSE (https://github.com/StartBootstrap/sb-admin-pro/blob/master/LICENSE)
    */
window.addEventListener('DOMContentLoaded', event => {
    // Activate feather
    feather.replace();

    // Enable tooltips globally
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Enable popovers globally
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Activate Bootstrap scrollspy for the sticky nav component
    const stickyNav = document.body.querySelector('#stickyNav');
    if (stickyNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#stickyNav',
            offset: 82,
        });
    }

    // Toggle the side navigation (Handled in base.html for better compatibility)
    /*
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sidenav-toggled'));
        });
    }
    */

    // Close side navigation when width < LG
    const sidenavContent = document.body.querySelector('#layoutSidenav_content');
    if (sidenavContent) {
        sidenavContent.addEventListener('click', event => {
            const BOOTSTRAP_LG_WIDTH = 992;
            if (window.innerWidth >= 992) {
                return;
            }
            if (document.body.classList.contains("sidenav-toggled")) {
                document.body.classList.toggle("sidenav-toggled");
            }
        });
    }

    // Add active state to sidebar nav links (FIX: Best Match Logic)
    const currentPath = window.location.pathname.replace(/\/$/, "");
    const targetAnchors = Array.from(document.body.querySelectorAll('.nav-link'));
    
    let bestMatch = null;
    let maxLen = -1;

    targetAnchors.forEach(targetAnchor => {
        const href = targetAnchor.getAttribute('href');
        if (!href || href === '#' || href === 'javascript:void(0);') return;

        // Normalizar href para comparación (quitar trailing slash)
        const normalizedHref = href.replace(/\/$/, "");

        // Check if exact match or if it's a parent path (followed by /)
        if (currentPath === normalizedHref || (normalizedHref !== "" && currentPath.startsWith(normalizedHref + "/"))) {
            // Quedarnos con el match más largo/específico
            if (normalizedHref.length > maxLen) {
                maxLen = normalizedHref.length;
                bestMatch = targetAnchor;
            }
        }
    });

    if (bestMatch) {
        bestMatch.classList.add('active');

        // Expand parent collapse menus
        let parentNode = bestMatch.parentNode;
        while (parentNode !== null && parentNode !== document.documentElement) {
            if (parentNode.classList.contains('collapse')) {
                parentNode.classList.add('show');
                const parentNavLink = document.body.querySelector(
                    '[data-bs-target="#' + parentNode.id + '"]'
                );
                if (parentNavLink) {
                    parentNavLink.classList.remove('collapsed');
                    parentNavLink.classList.add('active');
                }
            }
            parentNode = parentNode.parentNode;
        }
    }
});
