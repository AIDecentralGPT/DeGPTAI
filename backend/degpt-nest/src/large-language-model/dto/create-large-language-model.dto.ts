// login.dto.ts
import { IsString, IsNotEmpty } from 'class-validator';

export class CreateLargeLanguageModelDto {
  @IsString({ message: '输入内容必须是字符串' })
  @IsNotEmpty({ message: '输入内容不能为空' })
  content: string;
}
