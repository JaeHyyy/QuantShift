<template>
  <section class="panel">
    <h2 class="panel-title">최근 주문</h2>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>시간</th>
            <th>매수/매도</th>
            <th>가격</th>
            <th>수량</th>
            <th>상태</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td
              colspan="5"
              class="empty"
            >
              주문 내역 없음 · 거래소 연결 준비 중
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<style scoped>
.table-wrap {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

th,
td {
  text-align: left;
  padding: 8px 6px;
  border-bottom: 1px solid var(--border);
}

th {
  color: var(--text-muted);
  font-weight: 600;
  font-size: 11px;
}

.empty {
  color: var(--text-muted);
  text-align: center;
  padding: 20px 6px;
}
</style>
