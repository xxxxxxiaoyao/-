class ParticleBackground {
    constructor() {
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.canvas.className = 'interactive-bg';
        document.body.insertBefore(this.canvas, document.body.firstChild);

        this.particles = [];
        this.particleCount = 50;
        this.mouse = { x: 0, y: 0, radius: 100 };

        this.init();
        this.animate();
        this.addEventListeners();
    }

    init() {
        this.resize();
        this.createParticles();
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    createParticles() {
        this.particles = [];
        for (let i = 0; i < this.particleCount; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                radius: Math.random() * 2 + 1,
                baseX: Math.random() * this.canvas.width,
                baseY: Math.random() * this.canvas.height,
                density: (Math.random() * 30) + 1,
                color: `rgba(52, 152, 219, ${Math.random() * 0.3 + 0.2})` // 使用主题蓝色
            });
        }
    }

    addEventListeners() {
        window.addEventListener('resize', () => this.resize());
        
        window.addEventListener('mousemove', (e) => {
            this.mouse.x = e.clientX;
            this.mouse.y = e.clientY;
        });
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        this.particles.forEach(particle => {
            let dx = this.mouse.x - particle.x;
            let dy = this.mouse.y - particle.y;
            let distance = Math.sqrt(dx * dx + dy * dy);
            let forceDirectionX = dx / distance;
            let forceDirectionY = dy / distance;

            const maxDistance = this.mouse.radius;
            const force = (maxDistance - distance) / maxDistance;

            const directionX = forceDirectionX * force * particle.density;
            const directionY = forceDirectionY * force * particle.density;

            if (distance < this.mouse.radius) {
                particle.x -= directionX;
                particle.y -= directionY;
            } else {
                if (particle.x !== particle.baseX) {
                    dx = particle.x - particle.baseX;
                    particle.x -= dx/20;
                }
                if (particle.y !== particle.baseY) {
                    dy = particle.y - particle.baseY;
                    particle.y -= dy/20;
                }
            }

            // 绘制粒子
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
            this.ctx.fillStyle = particle.color;
            this.ctx.fill();

            // 连接临近的粒子
            this.particles.forEach(otherParticle => {
                const dx = particle.x - otherParticle.x;
                const dy = particle.y - otherParticle.y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < 100) {
                    this.ctx.beginPath();
                    this.ctx.strokeStyle = `rgba(52, 152, 219, ${0.1 * (1 - distance/100)})`;
                    this.ctx.lineWidth = 0.5;
                    this.ctx.moveTo(particle.x, particle.y);
                    this.ctx.lineTo(otherParticle.x, otherParticle.y);
                    this.ctx.stroke();
                }
            });
        });

        requestAnimationFrame(() => this.animate());
    }
}

// 当页面加载完成后初始化背景
window.addEventListener('load', () => {
    new ParticleBackground();
});