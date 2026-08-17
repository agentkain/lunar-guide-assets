import React from 'react';
import {Composition} from 'remotion';
import {AffirmStill, type AffirmStillProps} from './still';

const defaultProps: AffirmStillProps = {
  background: 'backgrounds/2026-08-23.png',
  date: 'AUGUST 23',
  message: 'Before September arrives, money will begin moving toward you in a new way.',
  format: 'story',
};

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="AffirmStory"
      component={AffirmStill}
      durationInFrames={1}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={defaultProps}
    />
    <Composition
      id="AffirmFeed"
      component={AffirmStill}
      durationInFrames={1}
      fps={30}
      width={1080}
      height={1350}
      defaultProps={{...defaultProps, format: 'feed'}}
    />
  </>
);
