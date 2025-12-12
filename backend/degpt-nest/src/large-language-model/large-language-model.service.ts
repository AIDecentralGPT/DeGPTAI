import { Injectable, InternalServerErrorException } from '@nestjs/common';
import { CreateLargeLanguageModelDto } from './dto/create-large-language-model.dto';
import { UpdateLargeLanguageModelDto } from './dto/update-large-language-model.dto';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { LargeMode } from './schemas/creatimg-schema';
import OpenAI from 'openai';

@Injectable()
export class LargeLanguageModelService {
  constructor(
    @InjectModel(LargeMode.name) private catModel: Model<LargeMode>,
  ) {}

  async create(createCatDto: CreateLargeLanguageModelDto) {
    const openai = new OpenAI({
      baseURL: 'https://api.deepseek.com',
      apiKey: 'sk-c9bd190ec2734f428dbebae295de81cd', // 建议换成环境变量
    });

    async function main() {
      const completion = await openai.chat.completions.create({
        messages: [{ role: 'user', content: createCatDto.content }],
        model: 'deepseek-reasoner',
      });

      return completion.choices[0].message.content;
    }

    try {
      // 关键：一定要 await，错误才会被 catch
      const result = await main();
      return { answer: result };
    } catch (error) {
      console.error('调用 deepseek 失败: ', error);
      // 不要直接 return error，建议抛 HTTP 异常
      throw new InternalServerErrorException('大模型服务异常');
    }
  }

  async findAll(): Promise<LargeMode[]> {
    return this.catModel.find().exec();
  }

  findOne(id: number) {
    return `This action returns a #${id} largeLanguageModel`;
  }

  update(id: number, updateLargeLanguageModelDto: UpdateLargeLanguageModelDto) {
    return `This action updates a #${id} largeLanguageModel`;
  }

  remove(id: number) {
    return `This action removes a #${id} largeLanguageModel`;
  }
}
