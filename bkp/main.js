import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

console.log('Iniciando aplicación GLB...');

// Configuración de la escena
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });

renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setClearColor(0x222222);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.body.appendChild(renderer.domElement);

// Controles de cámara
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;

// Iluminación
const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
directionalLight.position.set(5, 10, 5);
directionalLight.castShadow = true;
scene.add(directionalLight);

// Agregar un cubo de referencia temporal
const geometry = new THREE.BoxGeometry(0.5, 0.5, 0.5);
const material = new THREE.MeshPhongMaterial({ color: 0xff0000, transparent: true, opacity: 0.5 });
const referenceCube = new THREE.Mesh(geometry, material);
scene.add(referenceCube);
console.log('Cubo de referencia agregado');

// Posición inicial de la cámara
camera.position.set(0, 0, 5);

// Cargar modelo GLB
const loader = new GLTFLoader();

// CAMBIA ESTA RUTA POR LA DE TU ARCHIVO
const modelPath = './models/morphing_creatures.glb';

console.log('Intentando cargar modelo desde:', modelPath);

loader.load(
    modelPath,
    function (gltf) {
        console.log('✅ Modelo cargado exitosamente:', gltf);
        
        const model = gltf.scene;
        
        // Información del modelo
        console.log('Información del modelo:');
        console.log('- Escena:', model);
        console.log('- Hijos:', model.children);
        
        // Calcular el bounding box
        const box = new THREE.Box3().setFromObject(model);
        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3());
        
        console.log('- Centro:', center);
        console.log('- Tamaño:', size);
        
        // Configurar sombras
        model.traverse((child) => {
            if (child.isMesh) {
                child.castShadow = true;
                child.receiveShadow = true;
                console.log('- Mesh encontrado:', child.name || 'sin nombre');
            }
        });
        
        scene.add(model);
        console.log('Modelo agregado a la escena');
        
        // Ajustar cámara
        const maxDim = Math.max(size.x, size.y, size.z);
        if (maxDim > 0) {
            const fov = camera.fov * (Math.PI / 180);
            let cameraZ = Math.abs(maxDim / 2 * Math.tan(fov * 2)) * 1.5;
            
            camera.position.set(center.x, center.y, center.z + cameraZ);
            controls.target.copy(center);
            controls.update();
            
            console.log('Cámara ajustada a posición:', camera.position);
        }
        
        // Remover cubo de referencia
        scene.remove(referenceCube);
    },
    function (progress) {
        const percentage = (progress.loaded / progress.total * 100).toFixed(2);
        console.log('📥 Progreso de carga:', percentage + '%');
    },
    function (error) {
        console.error('❌ Error al cargar el modelo:', error);
        console.error('Verifica que el archivo existe en:', modelPath);
        
        // Mantener el cubo de referencia si hay error
        console.log('El cubo rojo indica que Three.js funciona, pero el modelo GLB no se cargó');
    }
);

// Redimensionar ventana
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// Loop de animación
function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}

animate();

console.log('Loop de renderizado iniciado');