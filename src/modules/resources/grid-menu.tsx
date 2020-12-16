import React from 'react'
import { List, ListItem, ListItemText } from 'opsramp-design-system'
import { useTranslation } from 'react-i18next'

const GridMenu: React.FC = () => {
  const { t } = useTranslation()
  return (
    <List className="body-1 ops-background rounded nav'-list">
      <ListItem key="test01">
        <ListItemText primaryText={t('grid.editColumns')} />
      </ListItem>
    </List>
  )
}

export default GridMenu
