import { Test, TestingModule } from '@nestjs/testing';
import { LargeLanguageModelController } from './large-language-model.controller';
import { LargeLanguageModelService } from './large-language-model.service';

describe('LargeLanguageModelController', () => {
  let controller: LargeLanguageModelController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [LargeLanguageModelController],
      providers: [LargeLanguageModelService],
    }).compile();

    controller = module.get<LargeLanguageModelController>(LargeLanguageModelController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
