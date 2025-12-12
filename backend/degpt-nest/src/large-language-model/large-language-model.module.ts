import { Module } from '@nestjs/common';
import { LargeLanguageModelService } from './large-language-model.service';
import { LargeLanguageModelController } from './large-language-model.controller';
import { LargeMode, LargeModeSchema } from './schemas/creatimg-schema';
import { MongooseModule } from '@nestjs/mongoose';

@Module({
  imports: [
    MongooseModule.forFeature([
      { name: LargeMode.name, schema: LargeModeSchema },
    ]),
  ],
  controllers: [LargeLanguageModelController],
  providers: [LargeLanguageModelService],
})
export class LargeLanguageModelModule {}
