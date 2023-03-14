import 'dotenv/config'
import { youtube } from '@googleapis/youtube'

const client = await youtube({
  version: 'v3',
  auth: process.env.GOOGLE_YOUTUBE_API_KEY,
})

const response = await client.videos.list({
  part: ['snippet'],
  id: ['11jpa8e5jEQ'],
})

console.log(response)
