import React from 'react';
import { motion } from 'framer-motion';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import { CheckCircle, AlertTriangle, XCircle, BookOpen, Code, ArrowRight } from 'lucide-react';
import { Button } from './Button';

interface ResultsDashboardProps {
  results: any;
  onReset: () => void;
}

export const ResultsDashboard: React.FC<ResultsDashboardProps> = ({ results, onReset }) => {
  const { ats_analysis, skill_gap, recommendations, llm_insights } = results;
  
  // Use LLM score if available, else ATS score
  const score = llm_insights?.ats_score?.score || ats_analysis.overall_score;
  const missingSkills = skill_gap.missing_skills;
  const projects = recommendations.recommended_projects;

  const scoreData = [
    { name: 'Score', value: score },
    { name: 'Remaining', value: 100 - score },
  ];

  const COLORS = [score >= 70 ? '#10B981' : score >= 50 ? '#F59E0B' : '#EF4444', '#E2E8F0'];

  return (
    <div className="w-full max-w-6xl mx-auto space-y-8 pb-20">
      {/* Header Section */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">Analysis Results</h2>
          <p className="text-slate-500">Target Role: {results.target_role_data.role}</p>
        </div>
        <Button variant="outline" onClick={onReset}>Analyze New Resume</Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Score Card */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 flex flex-col items-center justify-center col-span-1"
        >
          <h3 className="text-lg font-semibold text-slate-700 mb-4">ATS Compatibility Score</h3>
          <div className="h-48 w-full relative">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={scoreData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  startAngle={90}
                  endAngle={-270}
                  dataKey="value"
                  stroke="none"
                >
                  {scoreData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
            <div className="absolute inset-0 flex items-center justify-center flex-col">
              <span className={`text-4xl font-bold`} style={{ color: COLORS[0] }}>{Math.round(score)}%</span>
            </div>
          </div>
          <p className="text-center text-sm text-slate-500 mt-2 px-4">
            {llm_insights?.ats_score?.explanation || "Based on keyword matching and section analysis."}
          </p>
        </motion.div>

        {/* Skills Gap Analysis */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 col-span-1 md:col-span-2"
        >
          <h3 className="text-lg font-semibold text-slate-700 mb-4">Skill Gap Analysis</h3>
          <div className="space-y-4">
            {skill_gap.strong_matches.length > 0 && (
              <div className="flex flex-wrap gap-2">
                <span className="text-sm font-medium text-green-600 flex items-center gap-1">
                  <CheckCircle size={16} /> Strong Matches:
                </span>
                {skill_gap.strong_matches.map((skill: string) => (
                  <span key={skill} className="px-2 py-1 bg-green-50 text-green-700 text-xs rounded-full border border-green-100">
                    {skill}
                  </span>
                ))}
              </div>
            )}
            
            {skill_gap.weak_matches.length > 0 && (
              <div className="flex flex-wrap gap-2">
                <span className="text-sm font-medium text-amber-600 flex items-center gap-1">
                  <AlertTriangle size={16} /> Needs Improvement:
                </span>
                {skill_gap.weak_matches.map((m: any) => (
                  <span key={m.skill} className="px-2 py-1 bg-amber-50 text-amber-700 text-xs rounded-full border border-amber-100">
                    {m.skill} (Partial)
                  </span>
                ))}
              </div>
            )}

            <div className="flex flex-col gap-2">
              <span className="text-sm font-medium text-red-600 flex items-center gap-1">
                <XCircle size={16} /> Critical Missing Skills:
              </span>
              <div className="grid grid-cols-2 gap-2">
                {missingSkills.slice(0, 6).map((skill: string) => (
                  <div key={skill} className="p-2 bg-red-50 border border-red-100 rounded text-red-700 text-sm flex items-center justify-between">
                    {skill}
                    <a href={`https://www.google.com/search?q=learn+${skill}`} target="_blank" rel="noreferrer" className="text-red-400 hover:text-red-600">
                      <ArrowRight size={14} />
                    </a>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Recommended Projects */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <h3 className="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2">
          <Code className="text-primary" /> Recommended Projects
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((project: any, idx: number) => (
            <div key={idx} className="bg-white p-6 rounded-xl border border-slate-200 hover:border-primary hover:shadow-lg transition-all group">
              <div className="flex justify-between items-start mb-3">
                <h4 className="font-semibold text-lg text-slate-800 group-hover:text-primary transition-colors">{project.title}</h4>
                <span className="px-2 py-1 bg-slate-100 text-slate-600 text-xs rounded font-medium">{project.difficulty || "Intermediate"}</span>
              </div>
              <p className="text-slate-600 text-sm mb-4 line-clamp-3">{project.description}</p>
              
              <div className="mb-4">
                <p className="text-xs font-semibold text-slate-500 mb-2 uppercase tracking-wide">Tech Stack</p>
                <div className="flex flex-wrap gap-1">
                  {project.tech_stack.map((tech: string) => (
                    <span key={tech} className="px-2 py-1 bg-blue-50 text-blue-700 text-xs rounded">
                      {tech}
                    </span>
                  ))}
                </div>
              </div>

              <div className="bg-slate-50 p-3 rounded text-xs text-slate-700 italic border-l-2 border-primary">
                " {project.bullets ? project.bullets[0] : "Implement this to showcase your skills."} "
              </div>
            </div>
          ))}
        </div>
      </motion.div>

      {/* Learning Roadmap */}
      {llm_insights?.learning_roadmap && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-secondary text-white p-8 rounded-2xl"
        >
          <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
            <BookOpen className="text-accent" /> 3-Month Learning Roadmap
          </h3>
          <div className="space-y-6">
            {llm_insights.learning_roadmap.map((item: string, idx: number) => (
              <div key={idx} className="flex gap-4">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-accent text-secondary font-bold flex items-center justify-center">
                  {idx + 1}
                </div>
                <p className="pt-1 text-slate-300">{item}</p>
              </div>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  );
};
