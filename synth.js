class MorphSynth {
    constructor() {
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        this.masterGain = this.audioContext.createGain();
        this.masterGain.gain.value = 0.3;
        this.masterGain.connect(this.audioContext.destination);

        // Asegurarse de que el contexto está corriendo
        if (this.audioContext.state === 'suspended') {
            this.audioContext.resume();
        }
    }

    setVolume(value) {
        this.masterGain.gain.value = value * 0.5; // Multiplicamos por 0.5 para evitar distorsión
    }

    playCreatureSound(creature) {
        const osc = this.audioContext.createOscillator();
        const gain = this.audioContext.createGain();

        // Diferentes configuraciones para cada criatura
        const sounds = {
            jellyfish: { freq: 200, type: 'sine' },
            coral: { freq: 300, type: 'triangle' },
            octopus: { freq: 150, type: 'sawtooth' },
            flower: { freq: 400, type: 'sine' },
            cactus: { freq: 250, type: 'square' },
            fern: { freq: 350, type: 'triangle' }
        };

        const sound = sounds[creature] || sounds.jellyfish;

        osc.type = sound.type;
        osc.frequency.value = sound.freq;

        gain.gain.setValueAtTime(0.5, this.audioContext.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.5);

        osc.connect(gain);
        gain.connect(this.masterGain);

        osc.start();
        osc.stop(this.audioContext.currentTime + 0.5);
    }

    playMorphSound(value) {
        const osc = this.audioContext.createOscillator();
        const gain = this.audioContext.createGain();

        // Mapear valor del morph (0-1) a frecuencia (200-800Hz)
        const freq = 200 + (value * 600);

        osc.type = 'sine';
        osc.frequency.value = freq;

        gain.gain.setValueAtTime(0.2, this.audioContext.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.1);

        osc.connect(gain);
        gain.connect(this.masterGain);

        osc.start();
        osc.stop(this.audioContext.currentTime + 0.1);
    }
}

export default MorphSynth;
