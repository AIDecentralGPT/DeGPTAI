// large-language-model.db.ts
import { Model } from 'mongoose';
import { LargeMode } from '../large-language-model/schemas/creatimg-schema';
import { CreateLargeLanguageModelDto } from '../large-language-model/dto/create-large-language-model.dto';

export async function createLargeLanguageModel(
  model: Model<LargeMode>,
  dto: CreateLargeLanguageModelDto,
): Promise<LargeMode> {
  const createdCat = new model(dto);
  return createdCat.save();
}
