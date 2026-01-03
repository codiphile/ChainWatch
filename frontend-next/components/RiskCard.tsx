'use client';

import { motion } from 'framer-motion';
import { ReactNode } from 'react';
import { getSeverityColor } from '@/lib/utils';
import {
  Newspaper,
  CloudRain,
  Anchor,
  Thermometer,
  Wind,
  Droplets,
  Ship,
  Clock,
  AlertTriangle,
} from 'lucide-react';
import { NewsRisk, WeatherRisk, PortRisk } from '@/lib/types';

interface RiskCardProps {
  title: string;
  icon: ReactNode;
  severity: number;
  children: ReactNode;
  delay?: number;
}

function RiskCardBase({ title, icon, severity, children, delay = 0 }: RiskCardProps) {
  const color = getSeverityColor(severity);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
      className="glass-card rounded-2xl p-5 relative overflow-hidden group"
      style={{
        borderColor: `color-mix(in srgb, ${color} 30%, transparent)`,
      }}
    >
      {/* Glow effect on hover */}
      <motion.div
        className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500"
        style={{
          background: `radial-gradient(circle at 50% 0%, ${color}15 0%, transparent 70%)`,
        }}
      />

      {/* Header */}
      <div className="flex items-center justify-between mb-4 relative z-10">
        <div className="flex items-center gap-3">
          <div
            className="w-10 h-10 rounded-lg flex items-center justify-center"
            style={{
              background: `linear-gradient(135deg, ${color}30, ${color}10)`,
              border: `1px solid ${color}40`,
            }}
          >
            <span style={{ color }}>{icon}</span>
          </div>
          <div>
            <h3 className="font-display text-sm font-semibold tracking-wide text-white">
              {title}
            </h3>
          </div>
        </div>

        {/* Severity badge */}
        <div className="flex items-center gap-2">
          <span className="font-mono text-2xl font-bold" style={{ color }}>
            {severity}
          </span>
          <span className="text-slate-500 font-mono text-sm">/5</span>
        </div>
      </div>

      {/* Severity bar */}
      <div className="severity-bar mb-4">
        <motion.div
          className="severity-fill"
          style={{ background: color, color }}
          initial={{ width: 0 }}
          animate={{ width: `${(severity / 5) * 100}%` }}
          transition={{ duration: 0.8, delay: delay + 0.2 }}
        />
      </div>

      {/* Content */}
      <div className="relative z-10 space-y-3">{children}</div>
    </motion.div>
  );
}

// News Risk Card
export function NewsRiskCard({ data, delay }: { data: NewsRisk | null; delay?: number }) {
  if (!data) {
    return (
      <RiskCardBase
        title="NEWS RISK"
        icon={<Newspaper className="w-5 h-5" />}
        severity={1}
        delay={delay}
      >
        <p className="text-slate-500 text-sm">No data available</p>
      </RiskCardBase>
    );
  }

  return (
    <RiskCardBase
      title="NEWS RISK"
      icon={<Newspaper className="w-5 h-5" />}
      severity={data.severity}
      delay={delay}
    >
      <div className="flex items-center gap-2 text-xs">
        <AlertTriangle className="w-3 h-3 text-slate-400" />
        <span className="text-slate-400">Event Type:</span>
        <span className="font-mono text-white uppercase tracking-wide">
          {data.event_type}
        </span>
      </div>
      <p className="text-sm text-slate-300 leading-relaxed">{data.summary}</p>
      {data.sources.length > 0 && (
        <div className="flex flex-wrap gap-1 mt-2">
          {data.sources.slice(0, 3).map((source, i) => (
            <span
              key={i}
              className="px-2 py-0.5 bg-void-700/50 rounded text-xs text-slate-400 font-mono"
            >
              {source}
            </span>
          ))}
        </div>
      )}
    </RiskCardBase>
  );
}

// Weather Risk Card
export function WeatherRiskCard({ data, delay }: { data: WeatherRisk | null; delay?: number }) {
  if (!data) {
    return (
      <RiskCardBase
        title="WEATHER RISK"
        icon={<CloudRain className="w-5 h-5" />}
        severity={1}
        delay={delay}
      >
        <p className="text-slate-500 text-sm">No data available</p>
      </RiskCardBase>
    );
  }

  return (
    <RiskCardBase
      title="WEATHER RISK"
      icon={<CloudRain className="w-5 h-5" />}
      severity={data.severity}
      delay={delay}
    >
      <div className="grid grid-cols-3 gap-2 mb-3">
        {data.temperature_c !== null && (
          <div className="bg-void-700/30 rounded-lg p-2 text-center">
            <Thermometer className="w-4 h-4 text-slate-400 mx-auto mb-1" />
            <span className="font-mono text-sm text-white">{data.temperature_c.toFixed(1)}°C</span>
          </div>
        )}
        {data.wind_speed_kmh !== null && (
          <div className="bg-void-700/30 rounded-lg p-2 text-center">
            <Wind className="w-4 h-4 text-slate-400 mx-auto mb-1" />
            <span className="font-mono text-sm text-white">{data.wind_speed_kmh.toFixed(0)} km/h</span>
          </div>
        )}
        {data.rainfall_mm !== null && (
          <div className="bg-void-700/30 rounded-lg p-2 text-center">
            <Droplets className="w-4 h-4 text-slate-400 mx-auto mb-1" />
            <span className="font-mono text-sm text-white">{data.rainfall_mm.toFixed(1)} mm</span>
          </div>
        )}
      </div>
      <p className="text-sm text-slate-300 leading-relaxed">{data.details}</p>
    </RiskCardBase>
  );
}

// Port Risk Card
export function PortRiskCard({ data, delay }: { data: PortRisk | null; delay?: number }) {
  if (!data) {
    return (
      <RiskCardBase
        title="PORT CONGESTION"
        icon={<Anchor className="w-5 h-5" />}
        severity={1}
        delay={delay}
      >
        <p className="text-slate-500 text-sm">No data available</p>
      </RiskCardBase>
    );
  }

  const getCongestionColor = (level: string) => {
    switch (level) {
      case 'low': return '#10b981';
      case 'moderate': return '#f59e0b';
      case 'high': return '#ef4444';
      case 'critical': return '#dc2626';
      default: return '#64748b';
    }
  };

  return (
    <RiskCardBase
      title="PORT CONGESTION"
      icon={<Anchor className="w-5 h-5" />}
      severity={data.severity}
      delay={delay}
    >
      <div className="flex items-center gap-2 mb-3">
        <span
          className="px-3 py-1 rounded-full text-xs font-mono font-bold uppercase tracking-wider"
          style={{
            background: `${getCongestionColor(data.congestion_level)}20`,
            color: getCongestionColor(data.congestion_level),
            border: `1px solid ${getCongestionColor(data.congestion_level)}40`,
          }}
        >
          {data.congestion_level}
        </span>
      </div>
      <div className="grid grid-cols-2 gap-2 mb-3">
        {data.vessel_queue !== null && (
          <div className="bg-void-700/30 rounded-lg p-2 flex items-center gap-2">
            <Ship className="w-4 h-4 text-slate-400" />
            <div>
              <span className="font-mono text-sm text-white">{data.vessel_queue}</span>
              <span className="text-xs text-slate-500 ml-1">vessels</span>
            </div>
          </div>
        )}
        {data.avg_delay_hours !== null && (
          <div className="bg-void-700/30 rounded-lg p-2 flex items-center gap-2">
            <Clock className="w-4 h-4 text-slate-400" />
            <div>
              <span className="font-mono text-sm text-white">{data.avg_delay_hours.toFixed(0)}</span>
              <span className="text-xs text-slate-500 ml-1">hrs delay</span>
            </div>
          </div>
        )}
      </div>
      <p className="text-sm text-slate-300 leading-relaxed">{data.details}</p>
    </RiskCardBase>
  );
}
