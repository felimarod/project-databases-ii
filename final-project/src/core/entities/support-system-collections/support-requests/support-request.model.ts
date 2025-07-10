import { SlaMetrics } from "./sla-metrics.model";
import { UserAttachment } from "./user-attachments.model";
import { Response as SupportResponse } from "./responses.model";

export interface SupportRequest {
  _id: string;
  ticket_id: string;
  user_id: string;
  type: string;
  category: string;
  priority: string;
  status: string;
  subject: string;
  description: string;
  created_at: Date;
  updated_at: Date;
  resolved_at: Date | null;
  tags: string[];
  escalation_level: number;
  user_attachments: UserAttachment[];
  responses: SupportResponse[];
  sla_metrics: SlaMetrics;
}
