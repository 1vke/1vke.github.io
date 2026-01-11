document.addEventListener("DOMContentLoaded", function() {
	const starConfig = [
		{ id: 'stars', size: 1, desktopCount: 700, mobileCount: 200, duration: 50 },
		{ id: 'stars2', size: 2, desktopCount: 200, mobileCount: 75, duration: 100 },
		{ id: 'stars3', size: 3, desktopCount: 100, mobileCount: 30, duration: 150 }
	];

	// LCG stands for "Linear Congruential Generator". ✨ The more you know ✨
	function LCG(seed) {
		let state = seed;
		return function() {
			state = (1103515245 * state + 12345) % 2147483648;
			return state / 2147483648;
		};
	}

	const seed = 42069; // lol
	const rand = LCG(seed);

	function generateShadows(n) {
		let shadows = [];
		for (let i = 0; i < n; i++) {
			shadows.push(`${Math.floor(rand() * 100)}vw ${Math.floor(rand() * 200)}vh #ffffff7a`);
		}
		return shadows.join(', ');
	}

	const isMobile = window.innerWidth <= 768;

	starConfig.forEach(config => {
		const starDiv = document.getElementById(config.id);
		if (starDiv) {
			const count = isMobile ? config.mobileCount : config.desktopCount;
			const shadows = generateShadows(count);
			starDiv.style.boxShadow = shadows;
			
			const after = document.createElement('div');
			after.style.position = 'absolute';
			after.style.top = '200vh';
			after.style.width = `${config.size}px`;
			after.style.height = `${config.size}px`;
			after.style.background = 'transparent';
			after.style.boxShadow = shadows;
			starDiv.appendChild(after);
		}
	});

	function animateStars() {
		const now = Date.now();
		starConfig.forEach(config => {
			const starDiv = document.getElementById(config.id);
			if (starDiv) {
				const cycle = config.duration * 1000;
				const progress = (now % cycle) / cycle;
				const translateY = -200 * progress; // 200vh
				starDiv.style.transform = `translateY(${translateY}vh)`;
			}
		});
		requestAnimationFrame(animateStars);
	}

	animateStars();
});
