import { PerformanceMetrics } from "./performance-metrics.model";

export interface Agent {
  _id: string; // Unique identifier for the agent
  agent_id: string; // Unique agent identifier, used for internal tracking
  name: string; // Name of the agent
  email: string; // Email address of the agent
  department: string; // Department the agent belongs to
  status: string; // Current status of the agent (e.g., active, inactive)
  specializations: string[]; // Areas of expertise or specialization
  created_at: Date; // Date when the agent was created
  performance_metrics: PerformanceMetrics;
}
