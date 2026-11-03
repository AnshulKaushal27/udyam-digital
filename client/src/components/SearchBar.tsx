import React, { useState, useEffect } from 'react';
import { Search, X, Database } from 'lucide-react';

interface SearchBarProps {
  value: string;
  onChange: (val: string) => void;
  placeholder?: string;
  source?: string;
}

export const SearchBar: React.FC<SearchBarProps> = ({
  value,
  onChange,
  placeholder = 'Search recipient, sender, subject, or content...',
  source = 'elasticsearch',
}) => {
  const [localVal, setLocalVal] = useState(value);

  useEffect(() => {
    setLocalVal(value);
  }, [value]);

  useEffect(() => {
    const timer = setTimeout(() => {
      onChange(localVal);
    }, 350);

    return () => clearTimeout(timer);
  }, [localVal, onChange]);

  return (
    <div className="relative flex-1">
      <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
        <Search className="h-4 w-4 text-slate-400" />
      </div>
      <input
        type="text"
        value={localVal}
        onChange={(e) => setLocalVal(e.target.value)}
        placeholder={placeholder}
        className="w-full bg-slate-900 border border-slate-800 rounded-lg pl-10 pr-28 py-2 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 transition"
      />
      {localVal && (
        <button
          onClick={() => {
            setLocalVal('');
            onChange('');
          }}
          className="absolute inset-y-0 right-20 pr-2 flex items-center text-slate-400 hover:text-white"
        >
          <X className="w-3.5 h-3.5" />
        </button>
      )}
      <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
        <span className="flex items-center gap-1 text-[10px] font-medium text-slate-400 bg-slate-800/80 border border-slate-700/60 px-1.5 py-0.5 rounded">
          <Database className="w-2.5 h-2.5 text-blue-400" />
          {source === 'elasticsearch' ? 'Elasticsearch' : 'PostgreSQL'}
        </span>
      </div>
    </div>
  );
};
