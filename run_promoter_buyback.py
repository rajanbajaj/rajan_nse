from rajan_nse import Strategies

result = Strategies().promoterBuyBackStocks(delta=90, save_to_file=True)

print(f'\n{"Symbol":<20} {"Promoter Avg":>14} {"Last Price":>12} {"Diff %":>8}')
print('-' * 58)
for symbol, avg, last in result:
    diff = (last - avg) / abs(avg) * 100
    print(f'{symbol:<20} {avg:>14.2f} {last:>12.2f} {diff:>7.2f}%')
print(f'\nTotal: {len(result)} stocks found.')
