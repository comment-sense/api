import { Module } from '@nestjs/common'
import { AppController } from './app.controller'
import { AppService } from './app.service'
import { CommentsController } from './comments/comments.controller'

@Module({
  imports: [],
  controllers: [AppController, CommentsController],
  providers: [AppService],
})
export class AppModule {}
