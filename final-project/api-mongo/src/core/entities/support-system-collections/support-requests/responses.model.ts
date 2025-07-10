import { UserAttachment } from "./user-attachments.model";

export interface Response {
  response_id: string;
  agent_id: string;
  agent_name: string;
  message: string;
  response_type: string; // e.g., "text", "image", "file"
  timestamp: Date;
  attachments?: UserAttachment[]; // Optional, for file attachments
}
