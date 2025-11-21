import React, { useRef, useState, Suspense } from 'react';
import { useFrame, useLoader } from '@react-three/fiber';
import { Text, Html } from '@react-three/drei';
import * as THREE from 'three';
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader.js';

// Crown Model Component
function CrownModel({ hovered }: { hovered: boolean }) {
  const obj = useLoader(OBJLoader, '/models/crown.obj');
  const crownRef = useRef<THREE.Group>(null);

  // Clone and setup the crown
  const crown = React.useMemo(() => {
    const cloned = obj.clone();
    cloned.traverse((child) => {
      if (child instanceof THREE.Mesh) {
        child.material = new THREE.MeshStandardMaterial({
          color: '#ffd700',
          emissive: '#ffd700',
          emissiveIntensity: hovered ? 2 : 1.2,
          metalness: 0.9,
          roughness: 0.2,
        });
      }
    });
    return cloned;
  }, [obj, hovered]);

  useFrame((state) => {
    if (crownRef.current) {
      crownRef.current.rotation.z = state.clock.elapsedTime * 0.5;
    }
  });

  return <primitive ref={crownRef} object={crown} scale={0.03} position={[0, 1.2, 0]} rotation={[-Math.PI / 2, 0, 0]} />;
}

interface CandidateNodeProps {
  position: [number, number, number];
  candidate: any;
  onClick: (candidate: any) => void;
  color?: string;
  brightness?: number;
  hasRing?: boolean;
}

export default function CandidateNode({ position, candidate, onClick, color = '#3b82f6', brightness = 1, hasRing = false }: CandidateNodeProps) {
  const fishGroupRef = useRef<THREE.Group>(null);
  const bodyRef = useRef<THREE.Mesh>(null);
  const tailRef = useRef<THREE.Mesh>(null);
  const crownRef = useRef<THREE.Mesh>(null);
  const [hovered, setHover] = useState(false);

  // Scale up the entire fish for better visibility
  const fishScale = 1.5;

  // Swimming animation - circular motion around center
  useFrame((state, delta) => {
    if (fishGroupRef.current) {
      // Calculate the radius from center (distance from origin)
      const radius = Math.sqrt(position[0] * position[0] + position[2] * position[2]);

      // Circular swimming speed
      const speed = 0.15;
      const angle = state.clock.elapsedTime * speed + Math.atan2(position[2], position[0]);

      // Circular motion around center - update position
      const x = Math.cos(angle) * radius;
      const z = Math.sin(angle) * radius;
      const y = position[1] + Math.sin(state.clock.elapsedTime * 0.5 + position[0]) * 0.3;

      fishGroupRef.current.position.set(x, y, z);

      // Point fish in direction of movement (tangent to circle)
      fishGroupRef.current.rotation.y = angle + Math.PI / 2;

      // Gentle roll as they swim
      fishGroupRef.current.rotation.z = Math.sin(state.clock.elapsedTime * 0.4 + position[1]) * 0.1;
    }
    if (tailRef.current) {
      // Tail wagging motion
      tailRef.current.rotation.y = Math.sin(state.clock.elapsedTime * 3 + position[0]) * 0.4;
    }
  });

  return (
    <group ref={fishGroupRef} scale={fishScale}>
      {/* 3D Crown for top candidates (score >= 90) */}
      {hasRing && (
        <Suspense fallback={
          // Fallback torus while crown loads
          <mesh ref={crownRef} position={[0, 1.5, 0]} rotation={[0, 0, 0]}>
            <torusGeometry args={[0.8, 0.1, 8, 16]} />
            <meshStandardMaterial
              color="#ffd700"
              emissive="#ffd700"
              emissiveIntensity={hovered ? 2 : 1.2}
              metalness={0.8}
              roughness={0.2}
            />
          </mesh>
        }>
          <CrownModel hovered={hovered} />
        </Suspense>
      )}

      {/* Fish Body - main clickable area - more fish-like shape */}
      <mesh
        ref={bodyRef}
        onClick={(e) => {
          e.stopPropagation();
          onClick(candidate);
        }}
        onPointerOver={() => setHover(true)}
        onPointerOut={() => setHover(false)}
        rotation={[0, Math.PI / 2, 0]}
        scale={[1, 0.9, 0.7]}
      >
        <sphereGeometry args={[0.8, 16, 12]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={hovered ? brightness * 1.5 : brightness * 0.6}
          metalness={0.4}
          roughness={0.3}
        />
      </mesh>

      {/* Fish Head/Snout */}
      <mesh position={[0.7, 0, 0]} rotation={[0, Math.PI / 2, 0]}>
        <coneGeometry args={[0.4, 0.6, 12]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={hovered ? brightness * 1.3 : brightness * 0.5}
          metalness={0.4}
          roughness={0.3}
        />
      </mesh>

      {/* Fish Tail - diamond shape */}
      <mesh ref={tailRef} position={[-1.0, 0, 0]} rotation={[0, 0, Math.PI / 4]}>
        <coneGeometry args={[0.8, 1.4, 4]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={hovered ? brightness * 1.2 : brightness * 0.5}
          metalness={0.3}
          roughness={0.4}
          transparent
          opacity={0.9}
        />
      </mesh>

      {/* Top Dorsal Fin */}
      <mesh position={[-0.2, 0.7, 0]} rotation={[0, 0, 0]}>
        <coneGeometry args={[0.4, 0.9, 4]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={hovered ? brightness : brightness * 0.4}
          metalness={0.2}
          roughness={0.5}
          transparent
          opacity={0.85}
        />
      </mesh>

      {/* Side Pectoral Fins - more elegant */}
      <mesh position={[0.2, 0, 0.6]} rotation={[0.5, 0.3, Math.PI / 2.5]}>
        <coneGeometry args={[0.3, 0.7, 4]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={brightness * 0.4}
          metalness={0.2}
          roughness={0.5}
          transparent
          opacity={0.8}
        />
      </mesh>
      <mesh position={[0.2, 0, -0.6]} rotation={[-0.5, -0.3, -Math.PI / 2.5]}>
        <coneGeometry args={[0.3, 0.7, 4]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={brightness * 0.4}
          metalness={0.2}
          roughness={0.5}
          transparent
          opacity={0.8}
        />
      </mesh>

      {/* Bottom Fins */}
      <mesh position={[0.1, -0.5, 0]} rotation={[0, 0, Math.PI]}>
        <coneGeometry args={[0.2, 0.5, 4]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={brightness * 0.3}
          metalness={0.2}
          roughness={0.5}
          transparent
          opacity={0.75}
        />
      </mesh>

      {/* Eyes - positioned on the head/body */}
      <mesh position={[0.5, 0.35, 0.4]}>
        <sphereGeometry args={[0.18, 12, 12]} />
        <meshStandardMaterial
          color="#ffffff"
          emissive="#ffffff"
          emissiveIntensity={0.8}
          metalness={0.9}
          roughness={0.1}
        />
      </mesh>
      <mesh position={[0.5, 0.35, -0.4]}>
        <sphereGeometry args={[0.18, 12, 12]} />
        <meshStandardMaterial
          color="#ffffff"
          emissive="#ffffff"
          emissiveIntensity={0.8}
          metalness={0.9}
          roughness={0.1}
        />
      </mesh>

      {/* Eye pupils */}
      <mesh position={[0.65, 0.35, 0.42]}>
        <sphereGeometry args={[0.09, 8, 8]} />
        <meshStandardMaterial
          color="#000000"
          metalness={0.5}
          roughness={0.3}
        />
      </mesh>
      <mesh position={[0.65, 0.35, -0.42]}>
        <sphereGeometry args={[0.09, 8, 8]} />
        <meshStandardMaterial
          color="#000000"
          metalness={0.5}
          roughness={0.3}
        />
      </mesh>

      {hovered && (
        <Html distanceFactor={10}>
          <div className="bg-blue-900/90 text-white px-3 py-2 rounded-lg text-xs whitespace-nowrap pointer-events-none select-none backdrop-blur-sm border border-blue-400/50 shadow-lg">
            <div className="font-bold">{candidate.name}</div>
            <div className="text-blue-200 text-[10px]">Score: {candidate.score?.total_score || '?'}</div>
          </div>
        </Html>
      )}
    </group>
  );
}
