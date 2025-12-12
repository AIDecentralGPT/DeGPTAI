import { Test, TestingModule } from '@nestjs/testing';
import { LargeLanguageModelService } from './large-language-model.service';

describe('LargeLanguageModelService', () => {
  let service: LargeLanguageModelService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [LargeLanguageModelService],
    }).compile();

    service = module.get<LargeLanguageModelService>(LargeLanguageModelService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
