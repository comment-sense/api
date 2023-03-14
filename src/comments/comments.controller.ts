import { Controller, Get, Param } from '@nestjs/common'

@Controller('comments')
export class CommentsController {
  @Get()
  findAll() {
    return 'This action returns all comments'
  }

  @Get(':videoId')
  findOne(@Param('videoId') videoId) {
    return `This action returns a comments for video ${videoId}`
  }
}
