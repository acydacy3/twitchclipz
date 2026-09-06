import { Composition } from 'remotion';
import { AiflMain, AIFL_TOTAL } from './aifl/Main';
import { ProsperiShot, SHOT_DUR } from './kp/ProsperiShot';

export const Root: React.FC = () => {
  return (
    <>
      <Composition
        id="AiflPromo"
        component={AiflMain}
        durationInFrames={AIFL_TOTAL}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="ProsperiShot"
        component={ProsperiShot}
        durationInFrames={SHOT_DUR}
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
