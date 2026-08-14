import { defineCollection, z } from 'astro:content';

const events = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.string(),
    location: z.string(),
    description: z.string(),
    featured: z.boolean().default(false),
    url: z.string().optional(),
  }),
});

const writeups = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    pubDate: z.string(),
    score: z.string().optional(),
    place: z.string().optional(),
    tags: z.array(z.string()),
    challenges: z.array(
      z.object({
        name: z.string(),
        category: z.string(),
        points: z.string(),
      })
    ).default([]),
  }),
});

const projects = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.string(),
    tag: z.string(),
    description: z.string(),
    githubUrl: z.string().optional(),
    url: z.string().optional(),
  }),
});

const team = defineCollection({
  type: 'data',
  schema: z.object({
    handle: z.string(),
    role: z.string(),
    skills: z.array(z.string()).default([]),
  }),
});

export const collections = {
  events,
  writeups,
  projects,
  team,
};
