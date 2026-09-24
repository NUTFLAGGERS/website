import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const events = defineCollection({
  loader: glob({ pattern: '**/[^_]*.{md,mdx}', base: './src/content/events' }),
  schema: z.object({
    title: z.string(),
    date: z.string(),
    startDate: z.string().optional(),
    location: z.string().optional().default(''),
    description: z.string().optional().default(''),
    featured: z.boolean().default(false),
    draft: z.boolean().default(false),
    url: z.string().optional(),
    tags: z.array(z.string()).default([]),
    score: z.string().optional(),
    place: z.string().optional(),
    challenges: z.array(
      z.object({
        name: z.string(),
        category: z.string(),
        points: z.string(),
        writeupSlug: z.string().optional(),
      })
    ).default([]),
  }),
});

const writeups = defineCollection({
  loader: glob({ pattern: '**/[^_]*.{md,mdx}', base: './src/content/writeups' }),
  schema: z.object({
    title: z.string(),
    pubDate: z.string(),
    updatedDate: z.string().optional(),
    lastUpdated: z.string().optional(),
    event: z.string().optional(),
    author: z.string().optional(),
    description: z.string().optional(),
    score: z.string().optional(),
    draft: z.boolean().default(false),
    tags: z.array(z.string()).default([]),
  }),
});

const projects = defineCollection({
  loader: glob({ pattern: '**/[^_]*.{md,mdx}', base: './src/content/projects' }),
  schema: z.object({
    title: z.string(),
    date: z.string(),
    tag: z.string(),
    description: z.string(),
    featured: z.boolean().default(false),
    draft: z.boolean().default(false),
    githubUrl: z.string().optional(),
    url: z.string().optional(),
  }),
});

const team = defineCollection({
  loader: glob({ pattern: '**/[^_]*.json', base: './src/content/team' }),
  schema: z.object({
    handle: z.string(),
    role: z.string(),
    categories: z.array(z.string()).default([]),
    skills: z.array(z.string()).default([]),
    socials: z.record(z.string()).optional(),
    draft: z.boolean().default(false),
  }),
});

const resources = defineCollection({
  loader: glob({ pattern: '**/[^_]*.{md,mdx}', base: './src/content/resources' }),
  schema: z.object({
    title: z.string(),
    category: z.string(),
    description: z.string(),
    url: z.string(),
    tags: z.array(z.string()).default([]),
    featured: z.boolean().default(false),
    draft: z.boolean().default(false),
  }),
});

export const collections = {
  events,
  writeups,
  projects,
  team,
  resources,
};
