import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

interface BubblesProps {
  count?: number;
}

export default function Bubbles({ count = 200 }: BubblesProps) {
  const meshRef = useRef<THREE.InstancedMesh>(null);

  // Generate random bubble positions and properties
  const bubbles = useMemo(() => {
    const temp = [];
    for (let i = 0; i < count; i++) {
      const t = Math.random() * 100;
      const factor = 20 + Math.random() * 100;
      const speed = 0.01 + Math.random() * 0.3;
      const x = (Math.random() - 0.5) * 60;
      const y = (Math.random() - 0.5) * 60;
      const z = (Math.random() - 0.5) * 60;

      temp.push({ t, factor, speed, x, y, z, mx: 0, my: 0 });
    }
    return temp;
  }, [count]);

  // Dummy object for instancing
  const dummy = useMemo(() => new THREE.Object3D(), []);

  useFrame((state) => {
    if (!meshRef.current) return;

    bubbles.forEach((bubble, i) => {
      let { t, factor, speed, x, y, z } = bubble;

      // Slowly rise and drift
      t = bubble.t += speed / 2;
      const s = Math.cos(t);

      // Bubble rises
      y += speed * 0.5;

      // Reset to bottom when reaching top
      if (y > 30) {
        y = -30;
        bubble.y = y;
      }

      // Gentle drift
      const driftX = Math.sin(t * 0.5) * 2;
      const driftZ = Math.cos(t * 0.3) * 2;

      dummy.position.set(x + driftX, y, z + driftZ);

      // Vary bubble size slightly with time
      const scale = 0.1 + Math.sin(t * 2) * 0.05;
      dummy.scale.set(scale, scale, scale);

      dummy.updateMatrix();
      meshRef.current.setMatrixAt(i, dummy.matrix);
    });

    meshRef.current.instanceMatrix.needsUpdate = true;
  });

  return (
    <>
      <instancedMesh ref={meshRef} args={[undefined, undefined, count]}>
        <sphereGeometry args={[1, 8, 8]} />
        <meshStandardMaterial
          color="#ffffff"
          transparent
          opacity={0.3}
          metalness={0.1}
          roughness={0.1}
          envMapIntensity={0.5}
        />
      </instancedMesh>
    </>
  );
}
