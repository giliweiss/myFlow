import {
  ScreenContainer,
  EmptyState,
} from '../../../src/components/ui';
import { strings } from '../../../src/i18n/he';

export default function GroupProgressScreen() {
  return (
    <ScreenContainer>
      <EmptyState
        title={strings.progress.progress}
        message={strings.progress.comingSoonMessage}
        iconName="TrendingUp"
      />
    </ScreenContainer>
  );
}
