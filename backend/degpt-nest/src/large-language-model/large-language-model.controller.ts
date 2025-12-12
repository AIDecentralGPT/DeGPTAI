import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
} from '@nestjs/common';
import { LargeLanguageModelService } from './large-language-model.service';
import { CreateLargeLanguageModelDto } from './dto/create-large-language-model.dto';
import { UpdateLargeLanguageModelDto } from './dto/update-large-language-model.dto';

@Controller('large-language-model')
export class LargeLanguageModelController {
  constructor(
    private readonly largeLanguageModelService: LargeLanguageModelService,
  ) {}

  @Post()
  create(@Body() createLargeLanguageModelDto: CreateLargeLanguageModelDto) {
    return this.largeLanguageModelService.create(createLargeLanguageModelDto);
  }

  @Get()
  findAll() {
    return this.largeLanguageModelService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.largeLanguageModelService.findOne(+id);
  }

  @Patch(':id')
  update(
    @Param('id') id: string,
    @Body() updateLargeLanguageModelDto: UpdateLargeLanguageModelDto,
  ) {
    return this.largeLanguageModelService.update(
      +id,
      updateLargeLanguageModelDto,
    );
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.largeLanguageModelService.remove(+id);
  }
}
