import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

// Seaweed/Kelp component
function Kelp({ position }: { position: [number, number, number] }) {
  const kelpRef = useRef<THREE.Group>(null);
  const offset = useMemo(() => Math.random() * Math.PI * 2, []);

  useFrame((state) => {
    if (kelpRef.current) {
      // Gentle swaying motion
      kelpRef.current.rotation.z = Math.sin(state.clock.elapsedTime * 0.5 + offset) * 0.15;
    }
  });

  return (
    <group ref={kelpRef} position={position}>
      {/* Kelp stalk - multiple segments */}
      <mesh position={[0, 1, 0]}>
        <cylinderGeometry args={[0.1, 0.15, 2, 8]} />
        <meshStandardMaterial color="#1a4d2e" roughness={0.8} />
      </mesh>
      <mesh position={[0, 3, 0]}>
        <cylinderGeometry args={[0.08, 0.1, 2, 8]} />
        <meshStandardMaterial color="#1e5a35" roughness={0.8} />
      </mesh>
      <mesh position={[0.1, 4.8, 0]}>
        <cylinderGeometry args={[0.06, 0.08, 1.6, 8]} />
        <meshStandardMaterial color="#22703f" roughness={0.8} />
      </mesh>

      {/* Kelp leaves */}
      <mesh position={[0.3, 3.5, 0]} rotation={[0, 0, 0.3]}>
        <boxGeometry args={[0.6, 1.2, 0.05]} />
        <meshStandardMaterial color="#2d8a4e" roughness={0.7} />
      </mesh>
      <mesh position={[-0.3, 4, 0]} rotation={[0, 0, -0.3]}>
        <boxGeometry args={[0.5, 1, 0.05]} />
        <meshStandardMaterial color="#2d8a4e" roughness={0.7} />
      </mesh>
      <mesh position={[0.2, 5, 0]} rotation={[0, 0, 0.2]}>
        <boxGeometry args={[0.4, 0.8, 0.05]} />
        <meshStandardMaterial color="#35a05e" roughness={0.7} />
      </mesh>
    </group>
  );
}

// Rock component
function Rock({ position, scale = 1 }: { position: [number, number, number]; scale?: number }) {
  return (
    <mesh position={position} rotation={[0, Math.random() * Math.PI * 2, 0]}>
      <dodecahedronGeometry args={[scale, 0]} />
      <meshStandardMaterial color="#3d3d3d" roughness={0.9} />
    </mesh>
  );
}

// Coral component
function Coral({ position }: { position: [number, number, number] }) {
  return (
    <group position={position}>
      <mesh position={[0, 0.5, 0]}>
        <coneGeometry args={[0.3, 1, 6]} />
        <meshStandardMaterial color="#ff6b6b" emissive="#ff6b6b" emissiveIntensity={0.2} roughness={0.6} />
      </mesh>
      <mesh position={[0.4, 0.4, 0]}>
        <coneGeometry args={[0.2, 0.8, 6]} />
        <meshStandardMaterial color="#ee5a52" emissive="#ee5a52" emissiveIntensity={0.2} roughness={0.6} />
      </mesh>
      <mesh position={[-0.3, 0.3, 0.2]}>
        <coneGeometry args={[0.15, 0.6, 6]} />
        <meshStandardMaterial color="#ff8787" emissive="#ff8787" emissiveIntensity={0.2} roughness={0.6} />
      </mesh>
    </group>
  );
}

export default function OceanFloor() {
  // Generate random positions for ocean floor decorations
  const decorations = useMemo(() => {
    const kelps = [];
    const rocks = [];
    const corals = [];

    // Add kelp
    for (let i = 0; i < 15; i++) {
      const angle = (i / 15) * Math.PI * 2;
      const radius = 25 + Math.random() * 10;
      const x = Math.cos(angle) * radius;
      const z = Math.sin(angle) * radius;
      kelps.push([x, -30, z] as [number, number, number]);
    }

    // Add rocks
    for (let i = 0; i < 20; i++) {
      const angle = Math.random() * Math.PI * 2;
      const radius = 20 + Math.random() * 15;
      const x = Math.cos(angle) * radius;
      const z = Math.sin(angle) * radius;
      const scale = 0.5 + Math.random() * 1;
      rocks.push({ position: [x, -30, z] as [number, number, number], scale });
    }

    // Add coral
    for (let i = 0; i < 10; i++) {
      const angle = Math.random() * Math.PI * 2;
      const radius = 22 + Math.random() * 12;
      const x = Math.cos(angle) * radius;
      const z = Math.sin(angle) * radius;
      corals.push([x, -30, z] as [number, number, number]);
    }

    return { kelps, rocks, corals };
  }, []);

  return (
    <group>
      {/* Ocean floor plane */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -30, 0]} receiveShadow>
        <circleGeometry args={[50, 64]} />
        <meshStandardMaterial color="#1a3a4a" roughness={0.9} />
      </mesh>

      {/* Add kelp */}
      {decorations.kelps.map((pos, i) => (
        <Kelp key={`kelp-${i}`} position={pos} />
      ))}

      {/* Add rocks */}
      {decorations.rocks.map((rock, i) => (
        <Rock key={`rock-${i}`} position={rock.position} scale={rock.scale} />
      ))}

      {/* Add coral */}
      {decorations.corals.map((pos, i) => (
        <Coral key={`coral-${i}`} position={pos} />
      ))}
    </group>
  );
}
