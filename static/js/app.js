// GUN WiFi Tool - Enterprise Landing Page JavaScript
// Modular architecture with performance optimizations

(function() {
    'use strict';

    // Configuration
    const CONFIG = {
        animationDuration: {
            typing: 80,
            counter: 2000,
            fade: 800
        },
        terminal: {
            commands: [
                "$ python3 gun_wifi_tool.py --version",
                "GUN WiFi Tool v3.0 - Advanced Penetration Testing Suite",
                "",
                "$ python3 gun_wifi_tool.py --scan",
                "Scanning for wireless networks...",
                "[+] Found 8 networks in range",
                "[+] Enterprise_Corp - WPA2-Enterprise",
                "[+] Guest_Network - WPA2-PSK (Weak)",
                "[!] Hidden_SSID - WPS Enabled (Vulnerable)",
                "",
                "$ python3 gun_wifi_tool.py --evil-twin --ssid Free_WiFi",
                "Setting up Evil Twin Access Point...",
                "[+] Interface wlan0 set to monitor mode",
                "[+] Creating fake AP: Free_WiFi",
                "[+] Starting captive portal on port 8080",
                "[+] Google skin loaded successfully",
                "",
                "$ python3 gun_wifi_tool.py --deauth --target AA:BB:CC:DD:EE:FF",
                "Launching deauthentication attack...",
                "[+] Target: AA:BB:CC:DD:EE:FF",
                "[+] Sending 50 deauth packets",
                "[+] Client disconnected successfully",
                ""
            ]
        }
    };

    // Utility functions
    const Utils = {
        debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },

        throttle(func, limit) {
            let inThrottle;
            return function() {
                const args = arguments;
                const context = this;
                if (!inThrottle) {
                    func.apply(context, args);
                    inThrottle = true;
                    setTimeout(() => inThrottle = false, limit);
                }
            };
        },

        easeOutCubic(t) {
            return 1 - Math.pow(1 - t, 3);
        },

        copyToClipboard(text) {
            if (navigator.clipboard && window.isSecureContext) {
                return navigator.clipboard.writeText(text);
            } else {
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = text;
                textArea.style.position = 'fixed';
                textArea.style.left = '-999999px';
                textArea.style.top = '-999999px';
                document.body.appendChild(textArea);
                textArea.focus();
                textArea.select();
                
                return new Promise((resolve, reject) => {
                    document.execCommand('copy') ? resolve() : reject();
                    textArea.remove();
                });
            }
        },

        sanitizeInput(input) {
            if (typeof input !== 'string') return '';
            return input
                .replace(/[<>]/g, '') // Remove potential HTML tags
                .replace(/javascript:/gi, '') // Remove javascript: protocol
                .replace(/on\w+=/gi, '') // Remove event handlers
                .trim()
                .slice(0, 1000); // Limit length
        },

        escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        },

        validateUrl(url) {
            try {
                const urlObj = new URL(url);
                return ['http:', 'https:'].includes(urlObj.protocol);
            } catch {
                return false;
            }
        },

        showCopyFeedback(message = 'Copied to clipboard!') {
            // Remove existing feedback
            const existing = document.querySelector('.copy-feedback');
            if (existing) {
                existing.remove();
            }

            // Create new feedback
            const feedback = document.createElement('div');
            feedback.className = 'copy-feedback';
            feedback.textContent = message;
            document.body.appendChild(feedback);

            // Show and hide
            requestAnimationFrame(() => {
                feedback.classList.add('show');
                setTimeout(() => {
                    feedback.classList.remove('show');
                    setTimeout(() => feedback.remove(), 300);
                }, 2000);
            });
        }
    };

    // Terminal Animation Module
    const Terminal = {
        element: null,
        cursor: null,
        currentLine: 0,
        currentChar: 0,
        isRunning: false,

        init() {
            this.element = document.getElementById('terminal-content');
            this.cursor = document.querySelector('.terminal__cursor');
            
            if (this.element) {
                this.startAnimation();
            }
        },

        startAnimation() {
            if (this.isRunning) return;
            this.isRunning = true;
            this.typeNextChar();
        },

        typeNextChar() {
            if (this.currentLine >= CONFIG.terminal.commands.length) {
                // Animation complete, restart after delay
                setTimeout(() => {
                    this.reset();
                    this.startAnimation();
                }, 3000);
                return;
            }

            const currentCommand = CONFIG.terminal.commands[this.currentLine];
            
            if (this.currentChar >= currentCommand.length) {
                // Line complete, move to next
                this.element.innerHTML += '\n';
                this.currentLine++;
                this.currentChar = 0;
                
                // Add delay between lines
                const delay = currentCommand.startsWith('$') ? 500 : 200;
                setTimeout(() => this.typeNextChar(), delay);
                return;
            }

            // Type next character
            const char = currentCommand[this.currentChar];
            this.element.innerHTML += char;
            this.currentChar++;
            
            // Scroll terminal to bottom
            if (this.element.parentElement) {
                this.element.parentElement.scrollTop = this.element.parentElement.scrollHeight;
            }

            // Continue typing
            setTimeout(() => this.typeNextChar(), CONFIG.animationDuration.typing);
        },

        reset() {
            this.element.innerHTML = '';
            this.currentLine = 0;
            this.currentChar = 0;
            this.isRunning = false;
        }
    };

    // Counter Animation Module
    const CounterAnimation = {
        counters: [],
        observer: null,

        init() {
            this.counters = document.querySelectorAll('.stat__number');
            this.setupIntersectionObserver();
        },

        setupIntersectionObserver() {
            const options = {
                threshold: 0.5,
                rootMargin: '0px 0px -100px 0px'
            };

            this.observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
                        this.animateCounter(entry.target);
                    }
                });
            }, options);

            this.counters.forEach(counter => {
                this.observer.observe(counter);
            });
        },

        animateCounter(element) {
            element.classList.add('animated');
            const target = parseFloat(element.getAttribute('data-target'));
            const duration = CONFIG.animationDuration.counter;
            const startTime = performance.now();
            const isDecimal = target % 1 !== 0;
            const suffix = element.textContent.includes('+') ? '+' : 
                          element.textContent.includes('%') ? '%' : '';

            const animate = (currentTime) => {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const easedProgress = Utils.easeOutCubic(progress);
                
                let current = target * easedProgress;
                
                if (isDecimal) {
                    current = current.toFixed(1);
                } else {
                    current = Math.floor(current).toLocaleString();
                }

                element.textContent = current + suffix;

                if (progress < 1) {
                    requestAnimationFrame(animate);
                }
            };

            requestAnimationFrame(animate);
        }
    };

    // Theme Toggle Module
    const ThemeToggle = {
        toggle: null,
        icon: null,
        currentTheme: 'dark',

        init() {
            this.toggle = document.getElementById('theme-toggle');
            this.icon = this.toggle?.querySelector('.theme-toggle__icon');
            
            if (this.toggle) {
                this.loadSavedTheme();
                this.toggle.addEventListener('click', () => this.toggleTheme());
            }
        },

        loadSavedTheme() {
            // Check system preference or default to dark
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            this.currentTheme = prefersDark ? 'dark' : 'light';
            this.applyTheme();
        },

        toggleTheme() {
            this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
            this.applyTheme();
            
            // Add animation class
            this.toggle.style.transform = 'rotate(360deg)';
            setTimeout(() => {
                this.toggle.style.transform = '';
            }, 300);
        },

        applyTheme() {
            document.body.setAttribute('data-theme', this.currentTheme);
            if (this.icon) {
                this.icon.textContent = this.currentTheme === 'dark' ? '☀️' : '🌙';
            }
        }
    };

    // Navigation Module
    const Navigation = {
        nav: null,
        links: [],
        sections: [],

        init() {
            this.nav = document.getElementById('navbar');
            this.links = document.querySelectorAll('.nav__link[href^="#"]');
            this.sections = Array.from(this.links).map(link => {
                const id = link.getAttribute('href').substring(1);
                return document.getElementById(id);
            }).filter(Boolean);

            this.setupSmoothScroll();
            this.setupScrollSpy();
            this.setupNavbarBehavior();
        },

        setupSmoothScroll() {
            this.links.forEach(link => {
                link.addEventListener('click', (e) => {
                    e.preventDefault();
                    const targetId = link.getAttribute('href').substring(1);
                    const target = document.getElementById(targetId);
                    
                    if (target) {
                        const offsetTop = target.offsetTop - 80; // Account for fixed nav
                        window.scrollTo({
                            top: offsetTop,
                            behavior: 'smooth'
                        });
                    }
                });
            });
        },

        setupScrollSpy() {
            const options = {
                threshold: 0.3,
                rootMargin: '-80px 0px -80px 0px'
            };

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        this.setActiveLink(entry.target.id);
                    }
                });
            }, options);

            this.sections.forEach(section => {
                observer.observe(section);
            });
        },

        setActiveLink(activeId) {
            this.links.forEach(link => {
                const href = link.getAttribute('href').substring(1);
                link.classList.toggle('nav__link--active', href === activeId);
            });
        },

        setupNavbarBehavior() {
            let lastScrollY = window.scrollY;
            let isScrollingUp = false;

            const handleScroll = Utils.throttle(() => {
                const currentScrollY = window.scrollY;
                isScrollingUp = currentScrollY < lastScrollY;
                
                if (this.nav) {
                    // Add glass effect when scrolled
                    this.nav.classList.toggle('nav--scrolled', currentScrollY > 100);
                    
                    // Hide/show navbar on scroll (optional)
                    // this.nav.style.transform = isScrollingUp || currentScrollY < 100 ? 
                    //     'translateY(0)' : 'translateY(-100%)';
                }

                lastScrollY = currentScrollY;
            }, 16);

            window.addEventListener('scroll', handleScroll, { passive: true });
        }
    };

    // Installation Tabs Module
    const InstallationTabs = {
        tabs: [],
        panels: [],
        copyButtons: [],

        init() {
            this.tabs = document.querySelectorAll('.install-tab');
            this.panels = document.querySelectorAll('.install-panel');
            this.copyButtons = document.querySelectorAll('.code-block__copy');

            this.setupTabs();
            this.setupCopyButtons();
        },

        setupTabs() {
            this.tabs.forEach(tab => {
                tab.addEventListener('click', () => {
                    const targetTab = tab.getAttribute('data-tab');
                    this.switchTab(targetTab);
                });
            });
        },

        switchTab(activeTab) {
            // Update tab buttons
            this.tabs.forEach(tab => {
                tab.classList.toggle('active', tab.getAttribute('data-tab') === activeTab);
            });

            // Update panels
            this.panels.forEach(panel => {
                panel.classList.toggle('active', panel.id === activeTab);
            });
        },

        setupCopyButtons() {
            this.copyButtons.forEach(button => {
                button.addEventListener('click', async () => {
                    const codeId = button.getAttribute('data-copy');
                    const codeElement = document.getElementById(codeId);
                    
                    if (codeElement) {
                        try {
                            await Utils.copyToClipboard(codeElement.textContent);
                            Utils.showCopyFeedback();
                            
                            // Visual feedback on button
                            const originalText = button.textContent;
                            button.textContent = 'Copied!';
                            button.style.background = '#10b981';
                            
                            setTimeout(() => {
                                button.textContent = originalText;
                                button.style.background = '';
                            }, 2000);
                        } catch (err) {
                            Utils.showCopyFeedback('Failed to copy');
                            console.error('Copy failed:', err);
                        }
                    }
                });
            });
        }
    };

    // Scroll Animations Module
    const ScrollAnimations = {
        elements: [],
        observer: null,

        init() {
            this.elements = document.querySelectorAll('.feature-card, .download-card, .doc-card, .section__header');
            this.setupIntersectionObserver();
            this.addFadeInClasses();
        },

        addFadeInClasses() {
            this.elements.forEach(element => {
                element.classList.add('fade-in');
            });
        },

        setupIntersectionObserver() {
            const options = {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            };

            this.observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                    }
                });
            }, options);

            this.elements.forEach(element => {
                this.observer.observe(element);
            });
        }
    };

    // Performance Module
    const Performance = {
        init() {
            // Lazy loading images (if any were added)
            this.setupLazyLoading();
            
            // Preload critical resources
            this.preloadCriticalResources();
            
            // Monitor performance
            this.monitorPerformance();
        },

        setupLazyLoading() {
            const images = document.querySelectorAll('img[data-src]');
            
            if ('IntersectionObserver' in window && images.length > 0) {
                const imageObserver = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            const img = entry.target;
                            img.src = img.dataset.src;
                            img.classList.remove('lazy');
                            imageObserver.unobserve(img);
                        }
                    });
                });

                images.forEach(img => imageObserver.observe(img));
            }
        },

        preloadCriticalResources() {
            // Preload fonts
            const fontLink = document.createElement('link');
            fontLink.rel = 'preload';
            fontLink.as = 'font';
            fontLink.type = 'font/woff2';
            fontLink.crossOrigin = 'anonymous';
            fontLink.href = 'https://fonts.gstatic.com/s/outfit/v10/QGYpz_MVcBeNP4NjuGObqx1XmO1I4TC1C4G8.woff2';
            document.head.appendChild(fontLink);
        },

        monitorPerformance() {
            // Monitor Core Web Vitals (if needed for analytics)
            if ('PerformanceObserver' in window) {
                try {
                    const observer = new PerformanceObserver((entries) => {
                        entries.getEntries().forEach((entry) => {
                            // You can send this data to analytics
                            console.log(`${entry.name}: ${entry.value}`);
                        });
                    });

                    observer.observe({ entryTypes: ['largest-contentful-paint', 'first-input', 'cumulative-layout-shift'] });
                } catch (e) {
                    // Silently fail for unsupported browsers
                }
            }
        }
    };

    // Error Handling
    const ErrorHandler = {
        init() {
            window.addEventListener('error', this.handleError);
            window.addEventListener('unhandledrejection', this.handlePromiseRejection);
        },

        handleError(event) {
            console.error('JavaScript error:', event.error);
            // Could send to error reporting service
        },

        handlePromiseRejection(event) {
            console.error('Unhandled promise rejection:', event.reason);
            // Could send to error reporting service
        }
    };

    // Main Application
    const App = {
        init() {
            // Wait for DOM to be ready
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => this.start());
            } else {
                this.start();
            }
        },

        start() {
            try {
                // Initialize all modules
                ErrorHandler.init();
                Terminal.init();
                CounterAnimation.init();
                ThemeToggle.init();
                Navigation.init();
                InstallationTabs.init();
                ScrollAnimations.init();
                Performance.init();

                // Add loaded class for any CSS transitions
                document.body.classList.add('loaded');
                
                console.log('GUN WiFi Tool landing page initialized successfully');
            } catch (error) {
                console.error('Failed to initialize application:', error);
            }
        }
    };

    // Global utility functions for modal
    window.showCommands = function() {
        const modal = document.getElementById('commandsModal');
        if (modal) {
            modal.classList.add('modal--active');
            document.body.style.overflow = 'hidden';
        }
    };

    window.closeCommandsModal = function() {
        const modal = document.getElementById('commandsModal');
        if (modal) {
            modal.classList.remove('modal--active');
            document.body.style.overflow = '';
        }
    };

    window.copyCommand = function(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            const text = element.textContent || element.innerText;
            const sanitizedText = Utils.sanitizeInput(text);
            
            Utils.copyToClipboard(sanitizedText).then(() => {
                Utils.showCopyFeedback('Command copied to clipboard!');
            }).catch(() => {
                Utils.showCopyFeedback('Failed to copy command');
            });
        }
    };

    // Close modal when clicking outside
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal__backdrop')) {
            window.closeCommandsModal();
        }
    });

    // Close modal with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            window.closeCommandsModal();
        }
    });

    // Initialize the application
    App.init();

    // Expose utilities for debugging (development only)
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        window.GunWifiApp = {
            Terminal,
            CounterAnimation,
            ThemeToggle,
            Navigation,
            InstallationTabs,
            ScrollAnimations,
            Utils,
            CONFIG
        };
    }

})();