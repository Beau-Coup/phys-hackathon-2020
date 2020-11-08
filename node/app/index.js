import 'scss/_index.scss';
import * as THREE from 'three/build/three.min.js'
import 'three/examples/jsm/libs/stats.module.js';
import {TrackballControls} from 'three/examples/jsm/controls/TrackballControls';
import Stats from "three/examples/jsm/libs/stats.module";
import {TWEEN} from 'three/examples/jsm/libs/tween.module.min.js';
import $ from "jquery";
import SimplexNoise from "simplex-noise";
let controls;

let container, stats;

let camera, scene, renderer;

let crystals = [];
let numCrystals = 30;

let windowHalfX = window.innerWidth / 2;
let windowHalfY = window.innerHeight / 2;


const clocks = [];
const growthCompletions = [];
const growthTimeLimits = [];
const growthDelay = 0.05;
let light1, light2, light3, light4;
const material =  new THREE.MeshPhongMaterial( { color: 0xC0FBF7,opacity: 0.5, transparent: true,roughness: 0.1,metalness: 0.0, reflectivity: 0.7 } )

init();

function setCrystalColor(geometry1, count) {
    const color = new THREE.Color();
    const colors1 = geometry1.attributes.color;
    for (let i = 0; i < count; i++) {
        colors1.setXYZ(i, color.r, color.g, color.b);
    }
}


 function init() {
     $.get("snowflake", function(data, status){
    console.log(data);
    data = JSON.parse(data);
    numCrystals = data.length;
    container = document.getElementById('container');

    camera = new THREE.PerspectiveCamera(25, window.innerWidth / window.innerHeight, 1, 5000);

    camera.position.z = 1800;



    scene = new THREE.Scene();// scene.background = new THREE.Color(0xffffff);

    const light = new THREE.DirectionalLight(0xffffff);
    light.position.set(0, 0, 1);
    scene.add(light);

    const canvas = document.createElement('canvas');
    canvas.width = 128;
    canvas.height = 64;

    for (let i = 0; i < numCrystals; i++) {
        const radius = 7;
        const geometry1 = new THREE.DodecahedronBufferGeometry(radius, 1);
        const count = geometry1.attributes.position.count;
        geometry1.setAttribute('color', new THREE.BufferAttribute(new Float32Array(count * 3), 3));
        setCrystalColor(geometry1, count);
        const mesh = new THREE.Mesh(geometry1, material);
        mesh.position.x = data[i][0]*100
            mesh.position.y = data[i][1]*100,
            mesh.position.z = 0;
        mesh.scale.x = 0;
        mesh.scale.y = 0;
        mesh.scale.z = 0;
        crystals.push(mesh);
        scene.add(mesh);
    }


    for (let i = 0; i < numCrystals; i++) {
        clocks.push(new THREE.Clock);
        growthTimeLimits[i] = 3.0 + growthDelay * i;
        growthCompletions[i] = false;
    }

    renderer = new THREE.WebGLRenderer({antialias: true,alpha: true});
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(window.innerWidth, window.innerHeight);
    container.appendChild(renderer.domElement);

    controls = new TrackballControls(camera, renderer.domElement);

    stats = new Stats();
    container.appendChild(stats.dom);
    window.addEventListener('resize', onWindowResize, false);
         light1 = new THREE.PointLight(0xffffff,3);
        light1.position.set(0,300,500);
        scene.add(light1);
         light2 = new THREE.PointLight(0xffffff,3);
        light2.position.set(500,100,0);
        scene.add(light2);
         light3 = new THREE.PointLight(0xffffff,3);
        light3.position.set(0,100,-500);
        scene.add(light3);
         light4 = new THREE.PointLight(0xffffff,3);
        light4.position.set(-500,300,0);
        scene.add(light4);
        animate();
    });

}

function onWindowResize() {

    windowHalfX = window.innerWidth / 2;
    windowHalfY = window.innerHeight / 2;

    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    renderer.setSize(window.innerWidth, window.innerHeight);

}

function animate() {
    for (let i = 0; i < numCrystals; i++) {
        let mesh = crystals[i];
        if (!growthCompletions[i]) {
            let t = clocks[i].getElapsedTime();
            let timeElapsed = Math.max(0.0, t - growthTimeLimits[i] + 3.0);
            timeElapsed = Math.min(3.0, timeElapsed);
            if (timeElapsed >= growthTimeLimits[i]) {
                clocks[i] = new THREE.Clock;
                mesh.scale.set(1, 1, 1);
                growthCompletions[i] = true;
            } else {
                let mesh = crystals[i];
                mesh.scale.x = (timeElapsed / 3.0);
                mesh.scale.y = (timeElapsed / 3.0);
                mesh.scale.z = (timeElapsed / 3.0);
            }
        }
    }
    requestAnimationFrame(animate);

    controls.update();

    render();
    stats.update();

}

function render() {

    renderer.render(scene, camera);

}



App({ el: 'background' });

function App(conf) {
    let gArray = [];
    conf = {
        fov: 75,
        cameraZ: 75,
        xyCoef: 50,
        zCoef: 10,
        lightIntensity: 0.9,
        ambientColor: 0x000000,
        light1Color: 0x0E09DC,
        light2Color: 0x1CD1E1,
        light3Color: 0x18C02C,
        light4Color: 0xee3bcf,
        ...conf
    };

    let renderer, scene, camera, cameraCtrl;
    let width, height, cx, cy, wWidth, wHeight;
    const TMath = THREE.Math;

    let plane;
    const simplex = new SimplexNoise();

    const mouse = new THREE.Vector2();
    const mousePlane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0);
    const mousePosition = new THREE.Vector3();
    const raycaster = new THREE.Raycaster();

    const noiseInput = document.getElementById('noiseInput');
    const heightInput = document.getElementById('heightInput');

    init();

    function init() {
        renderer = new THREE.WebGLRenderer({ canvas: document.getElementById(conf.el), antialias: true, alpha: true });
        camera = new THREE.PerspectiveCamera(conf.fov);
        camera.position.z = conf.cameraZ;

        updateSize();
        initScene();
        animate();
    }


    function initScene() {
        scene = new THREE.Scene();
        initLights();

        let mat = new THREE.MeshLambertMaterial({ color: 0xffffff, side: THREE.DoubleSide });
        // let mat = new THREE.MeshPhongMaterial({ color: 0xffffff });
        // let mat = new THREE.MeshStandardMaterial({ color: 0x808080, roughness: 0.5, metalness: 0.8 });
        let geo = new THREE.PlaneBufferGeometry(wWidth, wHeight, wWidth / 2, wHeight / 2);
        plane = new THREE.Mesh(geo, mat);
        scene.add(plane);

        plane.rotation.x = -Math.PI / 2 - 0.2;
        plane.position.y = -25;
        camera.position.z = 60;
    }

    function initLights() {
        const r = 30;
        const y = 10;
        const lightDistance = 500;

        // light = new THREE.AmbientLight(conf.ambientColor);
        // scene.add(light);

        light1 = new THREE.PointLight(conf.light1Color, conf.lightIntensity, lightDistance);
        light1.position.set(0, y, r);
        scene.add(light1);
        light2 = new THREE.PointLight(conf.light2Color, conf.lightIntensity, lightDistance);
        light2.position.set(0, -y, -r);
        scene.add(light2);
        light3 = new THREE.PointLight(conf.light3Color, conf.lightIntensity, lightDistance);
        light3.position.set(r, y, 0);
        scene.add(light3);
        light4 = new THREE.PointLight(conf.light4Color, conf.lightIntensity, lightDistance);
        light4.position.set(-r, y, 0);
        scene.add(light4);
    }

    function animate() {
        requestAnimationFrame(animate);

        animatePlane();
        animateLights();

        renderer.render(scene, camera);
    };

    function animatePlane() {
        gArray = plane.geometry.attributes.position.array;
        const time = Date.now() * 0.0002;
        for (let i = 0; i < gArray.length; i += 3) {
            gArray[i + 2] = simplex.noise4D(gArray[i] / conf.xyCoef, gArray[i + 1] / conf.xyCoef, time, mouse.x + mouse.y) * conf.zCoef;
        }
        plane.geometry.attributes.position.needsUpdate = true;
        // plane.geometry.computeBoundingSphere();
    }

    function animateLights() {
        const time = Date.now() * 0.001;
        const d = 50;
        light1.position.x = Math.sin(time * 0.1) * d;
        light1.position.z = Math.cos(time * 0.2) * d;
        light2.position.x = Math.cos(time * 0.3) * d;
        light2.position.z = Math.sin(time * 0.4) * d;
        light3.position.x = Math.sin(time * 0.5) * d;
        light3.position.z = Math.sin(time * 0.6) * d;
        light4.position.x = Math.sin(time * 0.7) * d;
        light4.position.z = Math.cos(time * 0.8) * d;
    }

    function updateLightsColors() {
        conf.light1Color = chroma.random().hex();
        conf.light2Color = chroma.random().hex();
        conf.light3Color = chroma.random().hex();
        conf.light4Color = chroma.random().hex();
        light1.color = new THREE.Color(conf.light1Color);
        light2.color = new THREE.Color(conf.light2Color);
        light3.color = new THREE.Color(conf.light3Color);
        light4.color = new THREE.Color(conf.light4Color);
        // console.log(conf);
    }

    function updateSize() {
        width = window.innerWidth; cx = width / 2;
        height = window.innerHeight; cy = height / 2;
        if (renderer && camera) {
            renderer.setSize(width, height);
            camera.aspect = width / height;
            camera.updateProjectionMatrix();
            const wsize = getRendererSize();
            wWidth = wsize[0];
            wHeight = wsize[1];
        }
    }

    function getRendererSize() {
        const cam = new THREE.PerspectiveCamera(camera.fov, camera.aspect);
        const vFOV = cam.fov * Math.PI / 180;
        const height = 2 * Math.tan(vFOV / 2) * Math.abs(conf.cameraZ);
        const width = height * cam.aspect;
        return [width, height];
    }
}
