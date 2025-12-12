import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { LargeLanguageModelModule } from './large-language-model/large-language-model.module';
import { MongooseModule } from '@nestjs/mongoose';

@Module({
  imports: [
    LargeLanguageModelModule,
    MongooseModule.forRoot('mongodb://localhost:27017/degpt'), // 连接字符串
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
