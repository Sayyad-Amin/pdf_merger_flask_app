document.addEventListener('DOMContentLoaded', () => {
    // Mobile Menu Toggle
    const menuToggle = document.getElementById('menuToggle');
    const navbarMenu = document.querySelector('.navbar-menu');

    menuToggle.addEventListener('click', () => {
        navbarMenu.classList.toggle('active');
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.navbar-menu') && !e.target.closest('.menu-toggle')) {
            navbarMenu.classList.remove('active');
        }
    });

    // Close menu when clicking a nav link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            navbarMenu.classList.remove('active');
        });
    });

    // Close menu on window resize (if switching to desktop view)
    window.addEventListener('resize', () => {
        if (window.innerWidth > 768) {
            navbarMenu.classList.remove('active');
        }
    });

    // Modal Handlers with improved animations
    const howToUseLink = document.getElementById('howToUse');
    const aboutLink = document.getElementById('about');
    const tierInfoLink = document.getElementById('tierInfo');
    const pricingLink = document.getElementById('pricing');
    const howToUseModal = document.getElementById('howToUseModal');
    const aboutModal = document.getElementById('aboutModal');
    const tierInfoModal = document.getElementById('tierInfoModal');
    const pricingModal = document.getElementById('pricingModal');
    const closeButtons = document.querySelectorAll('.close-modal');

    // Show modals with smoother transitions
    howToUseLink.addEventListener('click', (e) => {
        e.preventDefault();
        closeAllModals();
        setTimeout(() => {
            howToUseModal.classList.add('active');
        }, 50); // Small delay for smoother animation
    });

    aboutLink.addEventListener('click', (e) => {
        e.preventDefault();
        closeAllModals();
        setTimeout(() => {
            aboutModal.classList.add('active');
        }, 50);
    });

    tierInfoLink.addEventListener('click', (e) => {
        e.preventDefault();
        closeAllModals();
        setTimeout(() => {
            tierInfoModal.classList.add('active');
        }, 50);
    });

    pricingLink.addEventListener('click', (e) => {
        e.preventDefault();
        closeAllModals();
        setTimeout(() => {
            pricingModal.classList.add('active');
        }, 50);
    });

    function closeAllModals() {
        [howToUseModal, aboutModal, tierInfoModal, pricingModal].forEach(modal => {
            modal.classList.remove('active');
        });
    }

    // Close modals with focus trap awareness
    closeButtons.forEach(button => {
        button.addEventListener('click', () => {
            closeAllModals();
        });
    });

    // Close modals on outside click with better UX
    [howToUseModal, aboutModal, tierInfoModal, pricingModal].forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                // Add small delay before removing class for smoother animation
                setTimeout(() => {
                    closeAllModals();
                }, 50);
            }
        });
    });

    // Close modals on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeAllModals();
        }
    });

    // Theme Management with proper transitions
    const html = document.documentElement;
    const themeToggle = document.getElementById('themeToggle');
    
    // Load saved theme
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);

    // Theme toggle button with proper icon transitions
    themeToggle.addEventListener('click', () => {
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        setTheme(newTheme);
        localStorage.setItem('theme', newTheme);
    });

    function setTheme(theme) {
        html.setAttribute('data-theme', theme);
        updateThemeIcons(theme);
    }

    function updateThemeIcons(theme) {
        const sunIcon = document.querySelector('.sun-icon');
        const moonIcon = document.querySelector('.moon-icon');
        
        if (theme === 'dark') {
            sunIcon.style.opacity = '1';
            sunIcon.style.transform = 'rotate(0) scale(1)';
            moonIcon.style.opacity = '0';
            moonIcon.style.transform = 'rotate(-90deg) scale(0)';
        } else {
            sunIcon.style.opacity = '0';
            sunIcon.style.transform = 'rotate(90deg) scale(0)';
            moonIcon.style.opacity = '1';
            moonIcon.style.transform = 'rotate(0) scale(1)';
        }
    }

    // Check system preference for initial theme if none saved
    if (!localStorage.getItem('theme')) {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        setTheme(prefersDark ? 'dark' : 'light');
        localStorage.setItem('theme', prefersDark ? 'dark' : 'light');
    }

    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) {
            setTheme(e.matches ? 'dark' : 'light');
        }
    });

    // File Upload and Processing with enhanced UX
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const fileList = document.getElementById('fileList');
    const mergeButton = document.getElementById('mergeButton');
    const uploadForm = document.getElementById('uploadForm');
    const progressContainer = document.getElementById('progressContainer');
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    const resultMessage = document.getElementById('resultMessage');
    
    let files = []; // Array to hold file objects
    
    // Premium toggle functionality 
    const premiumToggleButtons = document.querySelectorAll('.premium-toggle');
    
    premiumToggleButtons.forEach(button => {
        button.addEventListener('click', async () => {
            try {
                button.disabled = true;
                button.innerHTML = '<span class="loading-spinner"></span> Processing...';
                
                const response = await fetch('/toggle-premium', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                if (!response.ok) {
                    throw new Error('Failed to toggle premium status');
                }
                
                const data = await response.json();
                
                // Add animation for status change
                document.body.classList.add('tier-change-animation');
                
                // Update UI
                setTimeout(() => {
                    document.body.classList.remove('tier-change-animation');
                    updatePremiumStatus(data.is_premium);
                    location.reload(); // Refresh to update all UI elements
                }, 500);
                
            } catch (error) {
                console.error('Error:', error);
                showMessage(error.message || 'An error occurred', 'error');
            } finally {
                button.disabled = false;
                button.innerHTML = button.getAttribute('aria-label');
            }
        });
    });
    
    function updatePremiumStatus(isPremium) {
        const tierBadges = document.querySelectorAll('.tier-badge');
        const premiumStatus = document.querySelector('.premium-status');
        
        tierBadges.forEach(badge => {
            badge.textContent = isPremium ? 'Premium' : 'Free';
            badge.className = `tier-badge ${isPremium ? 'premium' : 'free'}`;
        });
        
        if (premiumStatus) {
            premiumStatus.textContent = isPremium ? 'Premium' : 'Free';
        }
    }
    
    // Enhanced form submission with better error handling and feedback
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        if (files.length === 0) {
            showMessage('Please select at least one PDF file', 'error');
            return;
        }
        
        if (files.length < 2) {
            showMessage('Please select at least 2 PDF files to merge', 'error');
            return;
        }
        
        // Show loading
        progressContainer.style.display = 'block';
        progressBar.style.width = '0%';
        progressText.textContent = '0%';
        mergeButton.disabled = true;
        
        try {
            // Create FormData from our files array
            const formData = new FormData();
            files.forEach(file => {
                formData.append('files[]', file);
            });
            
            // Add PDF format if available (premium feature)
            const pdfFormat = document.getElementById('pdfFormat');
            if (pdfFormat) {
                formData.append('pdf_format', pdfFormat.value);
            }
            
            // Add progress tracking
            const xhr = new XMLHttpRequest();
            xhr.open('POST', uploadForm.action);
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            
            // Progress updates with smooth animation
            xhr.upload.onprogress = (event) => {
                if (event.lengthComputable) {
                    const percentComplete = Math.round((event.loaded / event.total) * 100);
                    updateProgress(percentComplete);
                }
            };
            
            xhr.onload = function() {
                if (xhr.status >= 200 && xhr.status < 300) {
                    let response;
                    try {
                        response = JSON.parse(xhr.responseText);
                    } catch (e) {
                        console.error('Error parsing response:', e);
                        showMessage('Error processing server response', 'error');
                        resetForm();
                        return;
                    }
                    
                    // Show 100% progress
                    updateProgress(100);
                    
                    // Success animation
                    setTimeout(() => {
                        if (response.success) {
                            showSuccessWithDownload(response);
                            
                            // Automatically start download if URL is provided
                            if (response.download_url) {
                                const downloadLink = document.createElement('a');
                                downloadLink.href = response.download_url;
                                downloadLink.style.display = 'none';
                                document.body.appendChild(downloadLink);
                                downloadLink.click();
                                setTimeout(() => {
                                    document.body.removeChild(downloadLink);
                                }, 1000);
                            }
                        } else {
                            showMessage(response.error || 'An error occurred', 'error');
                        }
                        resetForm();
                    }, 500); // Delay for progress animation to complete
                    
                } else {
                    let errorMessage = 'Server error occurred';
                    try {
                        const response = JSON.parse(xhr.responseText);
                        errorMessage = response.error || errorMessage;
                    } catch(e) {
                        console.error('Error parsing response:', e);
                    }
                    showMessage(errorMessage, 'error');
                    resetForm();
                }
            };
            
            xhr.onerror = function() {
                showMessage('Connection error. Please try again.', 'error');
                resetForm();
            };
            
            // Handle timeouts gracefully
            xhr.timeout = 60000; // 60 seconds
            xhr.ontimeout = function() {
                showMessage('Request timed out. Your files might be too large.', 'error');
                resetForm();
            };
            
            // Send the form
            xhr.send(formData);
            
        } catch (error) {
            console.error('Error:', error);
            showMessage(error.message || 'An error occurred', 'error');
            resetForm();
        }
    });
    
    function updateProgress(percent) {
        // Smooth progress animation
        progressBar.style.transition = 'width 0.3s ease-in-out';
        progressBar.style.width = percent + '%';
        
        // Update text with animation
        const currentText = parseInt(progressText.textContent);
        animateNumber(currentText, percent, 300, value => {
            progressText.textContent = Math.round(value) + '%';
        });
    }
    
    function animateNumber(start, end, duration, callback) {
        const startTime = performance.now();
        
        function updateNumber(currentTime) {
            const elapsedTime = currentTime - startTime;
            if (elapsedTime >= duration) {
                callback(end);
                return;
            }
            
            const progress = elapsedTime / duration;
            const value = start + (end - start) * progress;
            callback(value);
            requestAnimationFrame(updateNumber);
        }
        
        requestAnimationFrame(updateNumber);
    }
    
    function showSuccessWithDownload(response) {
        resultMessage.className = 'alert alert-success';
        resultMessage.innerHTML = `
            <div class="success-message">
                <p>${response.message}</p>
                <a href="${response.download_url}" class="button download-button">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                        <polyline points="7 10 12 15 17 10"></polyline>
                        <line x1="12" y1="15" x2="12" y2="3"></line>
                    </svg>
                    Download PDF
                </a>
            </div>
        `;
        resultMessage.style.display = 'block';
        
        // Auto-scroll to result message
        setTimeout(() => {
            resultMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 300);
    }
    
    function resetForm() {
        // Enable button
        mergeButton.disabled = false;
        
        // Hide progress after a short delay
        setTimeout(() => {
            progressContainer.style.display = 'none';
        }, 500);
    }
    
    function showMessage(message, type) {
        resultMessage.className = `alert alert-${type}`;
        resultMessage.textContent = message;
        resultMessage.style.display = 'block';
        
        // Auto-scroll to message
        resultMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    
    // File handling with better drag and drop
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });
    
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });
    
    // Add the wiggle effect for dragover
    function highlight(e) {
        dropZone.classList.add('dragover');
        // Add wiggle animation class
        dropZone.classList.add('wiggle');
    }
    
    function unhighlight(e) {
        dropZone.classList.remove('dragover');
        // Remove wiggle animation class
        dropZone.classList.remove('wiggle');
    }
    
    dropZone.addEventListener('drop', handleDrop, false);
    fileInput.addEventListener('change', handleFileSelect, false);
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const droppedFiles = dt.files;
        handleFiles(droppedFiles);
    }
    
    function handleFileSelect(e) {
        const selectedFiles = e.target.files;
        handleFiles(selectedFiles);
    }
    
    function handleFiles(newFiles) {
        if (!newFiles || newFiles.length === 0) return;
        
        const validationResult = validateFiles(newFiles);
        if (!validationResult.valid) {
            showMessage(validationResult.message, 'error');
            return;
        }
        
        // Add files with animation
        Array.from(newFiles).forEach(file => {
            if (!files.some(f => f.name === file.name && f.size === file.size)) {
                files.push(file);
            }
        });
        
        updateFileList();
        fileInput.value = ''; // Reset file input
    }
    
    function updateFileList() {
        fileList.innerHTML = '';
        
        if (files.length === 0) {
            mergeButton.disabled = true;
            return;
        }
        
        // Sort files by name for better UX
        files.sort((a, b) => a.name.localeCompare(b.name));
        
        // Add files with staggered animation
        files.forEach((file, index) => {
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            fileItem.style.opacity = '0';
            fileItem.style.transform = 'translateY(10px)';
            
            const fileName = document.createElement('div');
            fileName.className = 'file-name';
            
            // Add file icon based on extension
            fileName.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                    <line x1="16" y1="13" x2="8" y2="13"></line>
                    <line x1="16" y1="17" x2="8" y2="17"></line>
                    <line x1="10" y1="9" x2="8" y2="9"></line>
                </svg>
                <span>${file.name}</span> <span class="file-size">(${formatFileSize(file.size)})</span>
            `;
            
            const removeButton = document.createElement('button');
            removeButton.className = 'remove-file';
            removeButton.innerHTML = '&times;';
            removeButton.setAttribute('aria-label', 'Remove file');
            removeButton.addEventListener('click', () => removeFile(index));
            
            fileItem.appendChild(fileName);
            fileItem.appendChild(removeButton);
            fileList.appendChild(fileItem);
            
            // Staggered animation
            setTimeout(() => {
                fileItem.style.opacity = '1';
                fileItem.style.transform = 'translateY(0)';
                fileItem.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            }, index * 50); // Stagger effect
        });
        
        // Enable merge button if there are files
        mergeButton.disabled = files.length < 1;
    }
    
    function formatFileSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
        else return (bytes / 1048576).toFixed(1) + ' MB';
    }
    
    function removeFile(index) {
        const fileElement = fileList.children[index];
        // Add removal animation
        fileElement.style.opacity = '0';
        fileElement.style.transform = 'translateX(10px)';
        
        setTimeout(() => {
            files.splice(index, 1);
            updateFileList();
        }, 300); // Wait for animation to complete
    }
    
    function validateFiles(fileList) {
        const pdfs = Array.from(fileList).filter(file => file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf'));
        
        if (pdfs.length === 0) {
            return { valid: false, message: 'Please select PDF files only' };
        }
        
        // Check if any of the files are not PDFs
        if (pdfs.length !== fileList.length) {
            return { valid: false, message: 'Only PDF files are allowed' };
        }
        
        // Success
        return { valid: true };
    }
    
    // Add keyboard accessibility
    dropZone.setAttribute('tabindex', '0');
    dropZone.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            fileInput.click();
        }
    });
    
    // Add wiggle animation keyframes to the CSS
    const style = document.createElement('style');
    style.textContent = `
        @keyframes wiggle {
            0%, 100% { transform: rotate(0deg); }
            25% { transform: rotate(-1deg) scale(1.01); }
            75% { transform: rotate(1deg) scale(1.01); }
        }
        
        .wiggle {
            animation: wiggle 0.5s ease-in-out;
        }
        
        .file-item {
            transition: opacity 0.3s ease, transform 0.3s ease;
        }
        
        .download-button {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            margin-top: 0.5rem;
        }
        
        .download-button svg {
            transition: transform 0.3s ease;
        }
        
        .download-button:hover svg {
            transform: translateY(3px);
        }
        
        .loading-spinner {
            display: inline-block;
            width: 1rem;
            height: 1rem;
            border: 2px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 0.8s linear infinite;
            margin-right: 0.5rem;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .tier-change-animation {
            animation: flash 0.5s ease-in-out;
        }
        
        @keyframes flash {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        .success-message {
            display: flex;
            flex-direction: column;
            align-items: center;
            animation: fadeInUp 0.5s ease-out;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    `;
    document.head.appendChild(style);
});