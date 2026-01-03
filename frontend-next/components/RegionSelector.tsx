'use client';

import { motion } from 'framer-motion';
import { MapPin, ChevronDown } from 'lucide-react';

interface RegionSelectorProps {
  regions: string[];
  selectedRegion: string;
  onSelect: (region: string) => void;
  disabled?: boolean;
}

export function RegionSelector({
  regions,
  selectedRegion,
  onSelect,
  disabled,
}: RegionSelectorProps) {
  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: 0.1 }}
      className="relative"
    >
      <label className="block text-xs font-mono text-slate-400 uppercase tracking-wider mb-2">
        <MapPin className="w-3 h-3 inline mr-1" />
        Target Region
      </label>
      <div className="relative">
        <select
          value={selectedRegion}
          onChange={(e) => onSelect(e.target.value)}
          disabled={disabled}
          className="select-cyber w-full min-w-[200px]"
        >
          {regions.map((region) => (
            <option key={region} value={region}>
              {region}
            </option>
          ))}
        </select>
      </div>
    </motion.div>
  );
}
