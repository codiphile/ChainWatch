'use client';

import { motion } from 'framer-motion';
import { Radar, Globe, ShieldCheck, Zap } from 'lucide-react';

export function EmptyState() {
  const features = [
    {
      icon: <Radar className="w-6 h-6" />,
      title: 'News Monitoring',
      description: 'AI-powered detection of supply chain disruptions, strikes, and policy changes.',
    },
    {
      icon: <Globe className="w-6 h-6" />,
      title: 'Weather Intelligence',
      description: 'Real-time weather analysis for port regions with impact assessment.',
    },
    {
      icon: <ShieldCheck className="w-6 h-6" />,
      title: 'Port Analytics',
      description: 'Congestion tracking, vessel queues, and delay predictions.',
    },
  ];

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay: 0.3 }}
      className="text-center py-12"
    >
      {/* Animated radar */}
      <motion.div
        className="relative w-32 h-32 mx-auto mb-8"
        initial={{ opacity: 0, scale: 0.5 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.4 }}
      >
        <div className="absolute inset-0 rounded-full border border-cyber-blue/30" />
        <div className="absolute inset-4 rounded-full border border-cyber-blue/20" />
        <div className="absolute inset-8 rounded-full border border-cyber-blue/10" />
        <motion.div
          className="absolute inset-0 rounded-full"
          style={{
            background: 'conic-gradient(from 0deg, transparent 0deg, rgba(6, 182, 212, 0.2) 60deg, transparent 120deg)',
          }}
          animate={{ rotate: 360 }}
          transition={{ duration: 4, repeat: Infinity, ease: 'linear' }}
        />
        <div className="absolute inset-0 flex items-center justify-center">
          <Zap className="w-8 h-8 text-cyber-blue" />
        </div>
      </motion.div>

      <motion.h2
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="font-display text-2xl font-bold tracking-wide text-white mb-3"
      >
        READY TO SCAN
      </motion.h2>

      <motion.p
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
        className="text-slate-400 mb-12 max-w-md mx-auto"
      >
        Select a region and initiate analysis to receive comprehensive supply chain risk intelligence.
      </motion.p>

      {/* Feature cards */}
      <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
        {features.map((feature, i) => (
          <motion.div
            key={feature.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7 + i * 0.1 }}
            className="glass-card rounded-xl p-6 text-left group hover:border-cyber-blue/30 transition-colors"
          >
            <div className="w-12 h-12 rounded-lg bg-cyber-blue/10 flex items-center justify-center mb-4 group-hover:bg-cyber-blue/20 transition-colors">
              <span className="text-cyber-blue">{feature.icon}</span>
            </div>
            <h3 className="font-display text-sm font-semibold tracking-wide text-white mb-2">
              {feature.title}
            </h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              {feature.description}
            </p>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
