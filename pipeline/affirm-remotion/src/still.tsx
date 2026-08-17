import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {loadFont as loadCormorant} from '@remotion/google-fonts/CormorantGaramond';
import {loadFont as loadMontserrat} from '@remotion/google-fonts/Montserrat';

const {fontFamily: serif} = loadCormorant('normal', {
  weights: ['500', '600'],
  subsets: ['latin'],
});
const {fontFamily: sans} = loadMontserrat('normal', {
  weights: ['400', '500', '600'],
  subsets: ['latin'],
});

export type AffirmStillProps = {
  background: string;
  date: string;
  message: string;
  format: 'feed' | 'story';
};

export const AffirmStill: React.FC<AffirmStillProps> = ({
  background,
  date,
  message,
  format,
}) => {
  const isStory = format === 'story';

  return (
    <AbsoluteFill style={{backgroundColor: '#100b18', color: '#fffaf2'}}>
      <Img
        src={staticFile(background)}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          filter: 'saturate(0.78) contrast(1.04) brightness(0.72)',
        }}
      />
      <AbsoluteFill
        style={{
          background:
            'linear-gradient(180deg, rgba(10,7,18,.48) 0%, rgba(20,10,29,.1) 27%, rgba(26,11,30,.2) 58%, rgba(9,6,15,.72) 100%)',
        }}
      />
      <AbsoluteFill
        style={{
          margin: isStory ? 54 : 46,
          border: '1px solid rgba(238,198,137,.34)',
          width: isStory ? 972 : 988,
          height: isStory ? 1812 : 1258,
        }}
      />

      <div
        style={{
          position: 'absolute',
          top: isStory ? 92 : 68,
          left: 0,
          right: 0,
          textAlign: 'center',
          fontFamily: sans,
          fontWeight: 500,
          fontSize: isStory ? 25 : 22,
          letterSpacing: 12,
          color: '#f1cf9a',
        }}
      >
        LUNAR <span style={{fontSize: 17}}>✦</span> GUIDE
      </div>

      <div
        style={{
          position: 'absolute',
          top: isStory ? 550 : 340,
          left: isStory ? 116 : 104,
          right: isStory ? 116 : 104,
          textAlign: 'center',
        }}
      >
        <div
          style={{
            fontFamily: sans,
            fontWeight: 500,
            fontSize: isStory ? 23 : 21,
            letterSpacing: 8,
            color: '#f1c98d',
            marginBottom: isStory ? 48 : 38,
          }}
        >
          {date} · A MESSAGE FOR YOU
        </div>
        <div
          style={{
            fontFamily: serif,
            fontWeight: 500,
            fontSize: isStory ? 78 : 66,
            lineHeight: 1.04,
            letterSpacing: -1.6,
            textWrap: 'balance',
            textShadow: '0 3px 24px rgba(0,0,0,.5)',
          }}
        >
          {message}
        </div>
      </div>

      <div
        style={{
          position: 'absolute',
          bottom: isStory ? 180 : 118,
          left: 0,
          right: 0,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: isStory ? 28 : 22,
        }}
      >
        <div
          style={{
            minWidth: isStory ? 610 : 570,
            padding: isStory ? '24px 40px' : '21px 36px',
            borderRadius: 999,
            textAlign: 'center',
            fontFamily: sans,
            fontWeight: 500,
            fontSize: isStory ? 28 : 25,
            letterSpacing: 1.1,
            color: '#1c1321',
            background: 'linear-gradient(180deg, #f7d89f, #dcae67)',
            boxShadow: '0 12px 34px rgba(0,0,0,.34)',
          }}
        >
          Comment <span style={{fontWeight: 600, letterSpacing: 3}}>AFFIRM</span> to lock it in
        </div>
        <div
          style={{
            fontFamily: sans,
            fontWeight: 400,
            fontSize: isStory ? 19 : 17,
            letterSpacing: 6,
            color: 'rgba(255,244,230,.7)',
          }}
        >
          @LUNARGUIDEAPP
        </div>
      </div>
    </AbsoluteFill>
  );
};
