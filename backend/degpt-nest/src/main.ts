import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ValidationPipe } from '@nestjs/common';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  // 自动校验参数
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true, // 自动剥离无关字段
      forbidNonWhitelisted: true, // 有不认识的字段直接报错
      transform: true, // 自动把json转换成对应的DTO对象
    }),
  );
  // 开启跨域
  app.enableCors({
    origin: true, // 也可以填写具体地址如 'http://154.198.49.172:6004'
    methods: 'GET,HEAD,PUT,PATCH,POST,DELETE,OPTIONS',
    credentials: true,
  });
  await app.listen(process.env.PORT ?? 3006);
}
bootstrap();
