import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document } from 'mongoose';

@Schema()
export class LargeMode extends Document {
  @Prop()
  content: string;
}

export const LargeModeSchema = SchemaFactory.createForClass(LargeMode);
