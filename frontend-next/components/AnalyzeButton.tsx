'use client';

import { motion } from 'framer-motion';
import { Radar, Loader2 } from 'lucide-react';

interface AnalyzeButtonProps {
  onClick: () => void;
  loading?: boolean;
  disabled?: boolean;
}

export function AnalyzeButton({ onClick, loading, disabled }: AnalyzeButtonProps) {
  return (
    <motion.button
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: 0.2 }}
      onClick={onClick}
      disabled={loading || disabled}
      className="btn-primary flex items-center gap-3"
      whileHover={{ scale: loading ? 1 : 1.02 }}
      whileTap={{ scale: loading ? 1 : 0.98 }}
    >
      {loading ? (
        <>
          <Loader2 className="w-5 h-5 animate-spin" />
          <span>Analyzing...</span>
        </>
      ) : (
        <>
          <Radar className="w-5 h-5" />
          <span>Analyze Region</span>
        </>
      )}
    </motion.button>
  );
}
