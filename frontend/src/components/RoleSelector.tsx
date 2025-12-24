import React from 'react';
import { motion } from 'framer-motion';
import { Code, Database, Server, Cpu, Layers, BarChart } from 'lucide-react';

interface RoleSelectorProps {
  selectedRole: string;
  onSelect: (role: string) => void;
}

const ROLES = [
  { id: "Frontend Developer", icon: Layers, color: "text-blue-500", bg: "bg-blue-100" },
  { id: "Backend Developer", icon: Server, color: "text-green-500", bg: "bg-green-100" },
  { id: "Full Stack Developer", icon: Code, color: "text-purple-500", bg: "bg-purple-100" },
  { id: "Machine Learning Engineer", icon: Cpu, color: "text-red-500", bg: "bg-red-100" },
  { id: "DevOps Engineer", icon: Database, color: "text-orange-500", bg: "bg-orange-100" },
  { id: "Data Scientist", icon: BarChart, color: "text-teal-500", bg: "bg-teal-100" },
];

export const RoleSelector: React.FC<RoleSelectorProps> = ({ selectedRole, onSelect }) => {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 gap-4 w-full max-w-4xl mx-auto">
      {ROLES.map((role) => {
        const Icon = role.icon;
        const isSelected = selectedRole === role.id;
        
        return (
          <motion.button
            key={role.id}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => onSelect(role.id)}
            className={`p-4 rounded-xl border-2 text-left transition-all flex flex-col gap-3
              ${isSelected 
                ? 'border-primary bg-blue-50 ring-2 ring-primary ring-offset-2' 
                : 'border-slate-200 bg-white hover:border-blue-200 hover:shadow-md'}
            `}
          >
            <div className={`p-2 rounded-lg w-fit ${role.bg} ${role.color}`}>
              <Icon size={24} />
            </div>
            <span className={`font-medium ${isSelected ? 'text-primary' : 'text-slate-700'}`}>
              {role.id}
            </span>
          </motion.button>
        );
      })}
    </div>
  );
};
