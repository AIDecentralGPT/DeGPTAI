import { PartialType } from '@nestjs/mapped-types';
import { CreateLargeLanguageModelDto } from './create-large-language-model.dto';

export class UpdateLargeLanguageModelDto extends PartialType(CreateLargeLanguageModelDto) {}
