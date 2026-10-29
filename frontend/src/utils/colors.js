// Deterministic color from a category name: same name -> same color across views.
export const stringToColor = (str) => {
  const value = String(str || 'Uncategorized')
  let hash = 0
  for (let i = 0; i < value.length; i++) {
    hash = value.charCodeAt(i) + ((hash << 5) - hash)
  }
  const h = Math.abs(hash) % 360
  return `hsl(${h}, 70%, 65%)`
}
