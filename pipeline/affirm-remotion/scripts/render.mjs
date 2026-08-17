import {readFileSync, mkdirSync, writeFileSync} from 'node:fs';
import {dirname, join, resolve} from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const scriptDir = dirname(fileURLToPath(import.meta.url));
const projectDir = resolve(scriptDir, '..');
const repoDir = resolve(projectDir, '..', '..');
const manifestPath = join(
  repoDir,
  'production',
  'affirm-2026-08-23-to-09-05.json',
);
const manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));
const renderLimit = Number.parseInt(process.env.RENDER_LIMIT ?? '0', 10);
const creatives = renderLimit
  ? manifest.creatives.slice(0, renderLimit)
  : manifest.creatives;

const getWeekMonday = (dateString) => {
  const date = new Date(`${dateString}T00:00:00Z`);
  const day = date.getUTCDay();
  const daysSinceMonday = day === 0 ? 6 : day - 1;
  date.setUTCDate(date.getUTCDate() - daysSinceMonday);
  return date.toISOString().slice(5, 10);
};

const getDateLabel = (dateString) =>
  new Intl.DateTimeFormat('en-US', {
    month: 'long',
    day: 'numeric',
    timeZone: 'UTC',
  })
    .format(new Date(`${dateString}T00:00:00Z`))
    .toUpperCase();

const runStill = ({composition, output, props}) => {
  mkdirSync(dirname(output), {recursive: true});
  const result = spawnSync(
    process.execPath,
    [
      join(projectDir, 'node_modules', '@remotion', 'cli', 'remotion-cli.js'),
      'still',
      'src/index.ts',
      composition,
      output,
      '--props',
      JSON.stringify(props),
      '--image-format',
      'jpeg',
      '--jpeg-quality',
      '95',
      '--log',
      'error',
    ],
    {cwd: projectDir, stdio: 'inherit'},
  );

  if (result.status !== 0) {
    throw new Error(
      `Remotion failed for ${output}: ${result.error?.message ?? `exit ${result.status}`}`,
    );
  }
};

const schedule = [];

for (const creative of creatives) {
  const [year, month] = creative.date.split('-');
  const week = `week-${getWeekMonday(creative.date)}`;
  const baseDir = join(repoDir, year, month, week);
  const baseName = `${creative.date}_08_AFFIRM`;
  const sharedProps = {
    background: `backgrounds/${creative.date}.png`,
    date: getDateLabel(creative.date),
    message: creative.message,
  };
  const feedPath = join(baseDir, 'feed', `${baseName}_4x5.jpg`);
  const storyPath = join(baseDir, 'stories', `${baseName}_9x16.jpg`);

  runStill({
    composition: 'AffirmFeed',
    output: feedPath,
    props: {...sharedProps, format: 'feed'},
  });
  runStill({
    composition: 'AffirmStory',
    output: storyPath,
    props: {...sharedProps, format: 'story'},
  });

  const caption = `${creative.message}

If this message found you, it is yours to claim.

✨ Comment AFFIRM to lock it in.

#affirmation #abundance #manifestation #goodthingsarecoming #trusttheprocess #spiritualgrowth #lunarguide`;
  mkdirSync(join(baseDir, 'captions'), {recursive: true});
  const captionPath = join(
    baseDir,
    'captions',
    `${creative.date}_AFFIRM_captions.txt`,
  );
  writeFileSync(captionPath, `${caption}\n`, 'utf8');

  schedule.push({
    date: creative.date,
    creativeId: creative.creativeId,
    message: creative.message,
    caption,
    feedPath: feedPath.slice(repoDir.length + 1).replaceAll('\\', '/'),
    storyPath: storyPath.slice(repoDir.length + 1).replaceAll('\\', '/'),
  });
  console.log(`Rendered ${creative.date}`);
}

writeFileSync(
  join(repoDir, 'production', 'affirm-buffer-schedule.json'),
  `${JSON.stringify(schedule, null, 2)}\n`,
  'utf8',
);
