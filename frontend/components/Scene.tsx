import React, { useState, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stars, Environment } from '@react-three/drei';
import CandidateNode from './CandidateNode';
import Bubbles from './Bubbles';
import OceanFloor from './OceanFloor';

interface SceneProps {
    candidates: any[];
    onCandidateSelect: (candidate: any) => void;
}

export default function Scene({ candidates, onCandidateSelect }: SceneProps) {
    // Generate vibrant rainbow colors based on candidate index for better distribution
    const getRainbowColor = (id: string, index: number, total: number) => {
        // Use golden ratio for better color distribution
        const goldenRatio = 0.618033988749895;
        const h = ((index * goldenRatio) % 1) * 360;
        const s = 85 + (Math.abs(Math.sin(index)) * 15); // 85-100% saturation
        const l = 55 + (Math.abs(Math.cos(index)) * 15); // 55-70% lightness
        return `hsl(${h}, ${s}%, ${l}%)`;
    };

    // Calculate positions in a spherical distribution
    const safeCandidates = candidates || [];
    const nodes = safeCandidates.map((candidate, i) => {
        const phi = Math.acos(-1 + (2 * i) / safeCandidates.length);
        const theta = Math.sqrt(safeCandidates.length * Math.PI) * phi;

        // Calculate radius based on score - higher scores are closer (smaller radius)
        const score = candidate.score?.total_score || 50;
        const baseRadius = 20;
        const minRadius = 8;
        // Map score (0-100) to radius (baseRadius to minRadius)
        const radius = baseRadius - ((score / 100) * (baseRadius - minRadius));

        return {
            ...candidate,
            position: [
                radius * Math.cos(theta) * Math.sin(phi),
                radius * Math.sin(theta) * Math.sin(phi),
                radius * Math.cos(phi)
            ] as [number, number, number],
            color: getRainbowColor(candidate.id || String(i), i, safeCandidates.length),
            brightness: 0.5 + (score / 100) * 1.5, // Higher score = brighter (0.5 to 2.0)
            hasRing: score >= 90 // Add red ring for top candidates
        };
    });

    return (
        <div className="w-full h-screen bg-gradient-to-b from-[#001a33] to-[#003d5c]">
            <Canvas
                camera={{ position: [0, 0, 25], fov: 60 }}
                dpr={[1, 2]}
                gl={{
                    antialias: true,
                    alpha: false,
                    powerPreference: 'high-performance',
                    precision: 'highp'
                }}
            >
                {/* Underwater gradient background */}
                <color attach="background" args={['#004d7a']} />
                {/* Underwater fog effect - bluish haze */}
                <fog attach="fog" args={['#003d5c', 15, 50]} />

                {/* Underwater lighting - brighter for better visibility */}
                <ambientLight intensity={1.0} color="#6ba3d1" />
                <directionalLight position={[10, 20, 10]} intensity={1.5} color="#b3d9f2" />
                <directionalLight position={[-10, -20, -10]} intensity={0.8} color="#7fc8f2" />
                <pointLight position={[-10, 10, -10]} intensity={0.8} color="#5fb8e6" />
                <pointLight position={[10, -10, 10]} intensity={0.6} color="#8dd5f7" />

                {/* Underwater bubbles rising */}
                <Bubbles count={200} />

                {/* Ocean floor with kelp, rocks, and coral */}
                <OceanFloor />

                <group>
                    {nodes.map((node, i) => (
                        <CandidateNode
                            key={node.id || i}
                            position={node.position}
                            candidate={node}
                            onClick={onCandidateSelect}
                            color={node.color}
                            brightness={node.brightness}
                            hasRing={node.hasRing}
                        />
                    ))}
                </group>

                <OrbitControls
                    enableZoom={true}
                    enablePan={true}
                    autoRotate
                    autoRotateSpeed={0.3}
                    maxDistance={35}
                    minDistance={5}
                />
            </Canvas>
        </div>
    );
}
